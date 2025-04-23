"""
Interactive TUI for PARA CLI.
"""
from pathlib import Path
import shutil
import subprocess
import platform
from typing import Optional, List
import time

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Tree, Static, Input, Label, Button, Select
from textual.widgets.tree import TreeNode
from textual import events
from textual.screen import ModalScreen
from textual.message import Message
from rich.text import Text

from .cli import DEFAULT_PARA_ROOT, CATEGORIES, get_visible_items, search_in_directory

class ActionModal(ModalScreen[bool]):
    """Modal for confirming actions."""

    def __init__(self, title: str, message: str):
        super().__init__()
        self.title = title
        self.message = message

    def compose(self) -> ComposeResult:
        yield Container(
            Label(self.title, id="action-title"),
            Static(self.message, id="action-message"),
            Horizontal(
                Button("Yes", variant="primary", id="yes"),
                Button("No", variant="error", id="no"),
                id="action-buttons",
            ),
            classes="action-container",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "yes":
            self.dismiss(True)
        else:
            self.dismiss(False)

class MoveModal(ModalScreen[Optional[str]]):
    """Modal for moving items."""

    def compose(self) -> ComposeResult:
        yield Container(
            Label("Move to Category", id="move-title"),
            Select(
                ((cat, cat) for cat in CATEGORIES),
                id="category-select",
                value=CATEGORIES[0]
            ),
            Horizontal(
                Button("Move", variant="primary", id="move"),
                Button("Cancel", variant="error", id="cancel"),
                id="move-buttons",
            ),
            classes="move-container",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "move":
            category = self.query_one("#category-select").value
            self.dismiss(category)
        else:
            self.dismiss(None)

class QuickSearchModal(ModalScreen[None]):
    """Quick search modal dialog."""

    class ResultAction(Message):
        """Message sent when an action is requested on a result."""
        def __init__(self, path: Path, action: str) -> None:
            self.path = path
            self.action = action
            super().__init__()

    BINDINGS = [
        ("escape", "cancel", "Cancel"),
        ("up", "previous_result", "Previous"),
        ("down", "next_result", "Next"),
        ("enter", "select_result", "Select"),
        ("delete", "delete_result", "Delete"),
        ("m", "move_result", "Move"),
        ("o", "open_result", "Open"),
    ]

    CSS = """
    Tree {
        width: 50%;
    }
    #details {
        width: 50%;
        padding: 1 2;
    }
    
    QuickSearchModal {
        align: center middle;
    }
    
    .quick-search-container {
        background: $surface;
        padding: 1 2;
        border: tall $primary;
        width: 60;
        height: auto;
    }
    
    #search-label {
        text-align: center;
        padding-bottom: 1;
    }
    
    #search-input {
        margin-bottom: 1;
    }
    
    #search-results {
        height: auto;
        max-height: 20;
    }

    .action-container {
        background: $surface;
        padding: 1 2;
        border: tall $primary;
        width: 40;
        height: auto;
    }

    #action-title {
        text-align: center;
        padding-bottom: 1;
    }

    #action-message {
        margin: 1 0;
    }

    #action-buttons {
        width: 100%;
        height: 3;
        align: center middle;
    }

    .move-container {
        background: $surface;
        padding: 1 2;
        border: tall $primary;
        width: 40;
        height: auto;
    }

    #move-title {
        text-align: center;
        padding-bottom: 1;
    }

    #category-select {
        margin: 1 0;
    }

    #move-buttons {
        width: 100%;
        height: 3;
        align: center middle;
    }
    """

    def __init__(self):
        super().__init__()
        self.results: List[Path] = []
        self.selected_index = 0

    def compose(self) -> ComposeResult:
        yield Container(
            Label("Search (type to search)", id="search-label"),
            Input(placeholder="Type to search...", id="search-input"),
            Static("", id="search-results"),
            Static("[Enter] Select  [Delete] Delete  [M] Move  [O] Open", id="search-help"),
            classes="quick-search-container",
        )

    def on_mount(self) -> None:
        """Focus the input when mounted."""
        self.query_one(Input).focus()

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle input changes."""
        query = event.value.strip()
        if len(query) >= 2:  # Only search for 2+ characters
            self.results = []
            for category in CATEGORIES:
                category_path = DEFAULT_PARA_ROOT / category
                self.results.extend(search_in_directory(category_path, query))
            
            self.selected_index = 0
            self._update_results_display()
        else:
            self.query_one("#search-results").update("")

    def on_key(self, event: events.Key) -> None:
        """Handle key events."""
        print(f"Key pressed: {event.key}")  # Debug print
        if event.key == "enter" and self.results:
            # Prevent the enter key from being handled by the input
            event.prevent_default()
            event.stop()
            self.action_select_result()
        elif event.key == "up":
            event.prevent_default()
            event.stop()
            self.action_previous_result()
        elif event.key == "down":
            event.prevent_default()
            event.stop()
            self.action_next_result()

    def _update_results_display(self) -> None:
        """Update the results display."""
        if not self.results:
            self.query_one("#search-results").update("[dim]No matches found[/]")
            return

        content = []
        for i, path in enumerate(self.results[:10]):  # Show top 10 results
            prefix = ">" if i == self.selected_index else " "
            rel_path = path.relative_to(DEFAULT_PARA_ROOT)
            category = rel_path.parts[0]
            name = path.name
            
            if i == self.selected_index:
                line = f"[bold cyan]{prefix} {category} / {name}[/]"
            else:
                line = f"[dim]{prefix} {category} / {name}[/]"
            content.append(line)

        if len(self.results) > 10:
            content.append("[dim]... and more results[/]")

        self.query_one("#search-results").update("\n".join(content))

    async def action_delete_result(self) -> None:
        """Delete the selected result."""
        if not self.results or self.selected_index >= len(self.results):
            return

        path = self.results[self.selected_index]
        confirm = await self.app.push_screen(
            ActionModal(
                "Confirm Delete",
                f"Are you sure you want to delete:\n{path.name}?"
            )
        )
        
        if confirm:
            self.post_message(self.ResultAction(path, "delete"))
            self.app.pop_screen()

    async def action_move_result(self) -> None:
        """Move the selected result."""
        if not self.results or self.selected_index >= len(self.results):
            return

        path = self.results[self.selected_index]
        new_category = await self.app.push_screen(MoveModal())
        
        if new_category:
            self.post_message(self.ResultAction(path, f"move:{new_category}"))
            self.app.pop_screen()

    def action_previous_result(self) -> None:
        """Select previous result."""
        if self.results:
            self.selected_index = (self.selected_index - 1) % len(self.results)
            self._update_results_display()

    def action_next_result(self) -> None:
        """Select next result."""
        if self.results:
            self.selected_index = (self.selected_index + 1) % len(self.results)
            self._update_results_display()

    def action_select_result(self) -> None:
        """Select the current result."""
        if self.results and 0 <= self.selected_index < len(self.results):
            self.post_message(self.ResultAction(self.results[self.selected_index], "select"))
            self.app.pop_screen()

    def action_cancel(self) -> None:
        """Cancel the search."""
        self.app.pop_screen()

    def action_open_result(self) -> None:
        """Open the selected result with default application."""
        if self.results and 0 <= self.selected_index < len(self.results):
            self.post_message(self.ResultAction(self.results[self.selected_index], "open"))
            self.app.pop_screen()

class ParaApp(App):
    """A Textual app to manage PARA system."""
    
    CSS = """
    Tree {
        width: 100%;
    }

    Tree.with-preview {
        width: 60%;
    }
    
    #details {
        width: 40%;
        padding: 1 2;
        display: none;
    }

    #details.show {
        display: block;
    }
    
    QuickSearchModal {
        align: center middle;
    }
    
    .quick-search-container {
        background: $surface;
        padding: 1 2;
        border: tall $primary;
        width: 60;
        height: auto;
    }
    
    #search-label {
        text-align: center;
        padding-bottom: 1;
    }
    
    #search-input {
        margin-bottom: 1;
    }
    
    #search-results {
        height: auto;
        max-height: 20;
    }
    """
    
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh"),
        ("f", "search", "Search"),
        ("n", "new_item", "New Item"),
        ("d", "delete", "Delete"),
        ("m", "move", "Move"),
        ("o", "open_selected", "Open in System"),
        ("p", "toggle_preview", "Toggle Preview"),
        ("enter", "select_node", "Select"),
        ("space", "toggle_node", "Expand/Collapse"),
    ]

    def __init__(self):
        super().__init__()
        self.current_path: Optional[Path] = None
        self.show_preview = False
        self.last_shift_press = 0.0

    def on_key(self, event: events.Key) -> None:
        """Handle key events for double shift detection."""
        if event.key == "shift":
            current_time = time.time()
            if current_time - self.last_shift_press < 0.3:  # 300ms threshold for double press
                self.action_quick_search()
            self.last_shift_press = current_time

    def action_quick_search(self) -> None:
        """Show quick search modal."""
        self.push_screen(QuickSearchModal())

    def select_path(self, path: Path) -> None:
        """Select a path in the tree view."""
        self.current_path = path
        self.show_details(path)
        
        # Expand tree to the selected path
        tree = self.query_one(Tree)
        current = tree.root
        
        # Build path parts relative to PARA root
        try:
            rel_path = path.relative_to(DEFAULT_PARA_ROOT)
            path_parts = list(rel_path.parts)
            
            # Navigate and expand tree nodes
            for part in path_parts:
                found = False
                for node in current.children:
                    node_name = str(node.label).split(" ", 1)[0]
                    if node_name.startswith("📁 "):
                        node_name = node_name[2:]
                    if node_name == part:
                        current = node
                        current.expand()
                        found = True
                        break
                if not found:
                    break
            
            # Select the final node
            if current != tree.root:
                tree.select_node(current)
                
        except Exception as e:
            self.notify(f"Error navigating to path: {e}")

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Container(
            Horizontal(
                Tree("PARA", "para"),
                Static("Press 'p' to show preview", id="details"),
            )
        )
        yield Footer()

    def on_mount(self) -> None:
        """Set up the app when mounted."""
        self.refresh_tree()
        # Start with preview hidden
        self.query_one(Tree).remove_class("with-preview")
        self.query_one("#details").remove_class("show")

    def refresh_tree(self) -> None:
        """Refresh the directory tree."""
        tree = self.query_one(Tree)
        tree.clear()
        
        root = tree.root
        root.set_label(Text(f"PARA ({DEFAULT_PARA_ROOT})"))
        root.expand()
        
        for category in CATEGORIES:
            category_path = DEFAULT_PARA_ROOT / category
            if category_path.exists():
                folders, files = get_visible_items(category_path)
                cat_node = root.add(f"{category} ({folders} folders, {files} files)")
                self._add_directory(cat_node, category_path)

    def _add_directory(self, node: TreeNode, path: Path) -> None:
        """Recursively add directory contents to the tree."""
        try:
            # Sort directories first, then files
            paths = sorted(
                [p for p in path.iterdir() if not p.name.startswith('.')],
                key=lambda p: (not p.is_dir(), p.name.lower())
            )
            
            for item in paths:
                if item.is_dir():
                    item_node = node.add(f"📁 {item.name}")
                    self._add_directory(item_node, item)
                else:
                    # Add files without allowing them to expand
                    node.add_leaf(f"📄 {item.name}")
        except Exception as e:
            node.add(f"[red]Error: {str(e)}[/]")

    def action_toggle_node(self) -> None:
        """Toggle expansion of the selected node."""
        tree = self.query_one(Tree)
        if tree.cursor_node:
            if tree.cursor_node.is_expanded:
                tree.cursor_node.collapse()
            else:
                tree.cursor_node.expand()

    def action_select_node(self) -> None:
        """Handle Enter key on a node."""
        tree = self.query_one(Tree)
        if not tree.cursor_node:
            return

        # Process the selection to update current_path and show preview
        self._process_node_selection(tree.cursor_node)
        
        # Only toggle expansion for folders
        if tree.cursor_node.allow_expand:
            if tree.cursor_node.is_expanded:
                tree.cursor_node.collapse()
            else:
                tree.cursor_node.expand()

    def _process_node_selection(self, node: TreeNode) -> None:
        """Process the selection of a tree node."""
        path_parts = []
        current = node
        
        # Build the full path from node hierarchy
        while current.parent is not None:
            label = str(current.label)
            
            # Handle different node types
            if " (" in label:  # Category nodes with counts
                category = label.split(" (")[0]
                if category in CATEGORIES:
                    path_parts.insert(0, category)
            elif " " in label:  # File/folder nodes with icons
                name = label.split(" ", 1)[1]
                path_parts.insert(0, name)
            else:
                # Skip any other nodes (like root)
                pass
            
            current = current.parent
        
        if path_parts:
            self.current_path = DEFAULT_PARA_ROOT.joinpath(*path_parts)
            if self.show_preview:
                self.show_details(self.current_path)

    def action_toggle_preview(self) -> None:
        """Toggle the preview panel."""
        self.show_preview = not self.show_preview
        tree = self.query_one(Tree)
        details = self.query_one("#details")
        
        if self.show_preview:
            tree.add_class("with-preview")
            details.add_class("show")
            if self.current_path:
                self.show_details(self.current_path)
        else:
            tree.remove_class("with-preview")
            details.remove_class("show")

    def show_details(self, path: Path) -> None:
        """Show details of selected item."""
        if not self.show_preview:
            return

        details = self.query_one("#details")
        
        if not path.exists():
            details.update(f"[red]Path does not exist: {path}[/]")
            return
        
        content = []
        content.append(f"[bold blue]{path.name}[/]")
        
        if path.is_dir():
            folders, files = get_visible_items(path)
            content.append(f"{folders} folders, {files} files")
            
            # Show first level of contents for directories
            try:
                items = sorted(
                    [p for p in path.iterdir() if not p.name.startswith('.')],
                    key=lambda p: (not p.is_dir(), p.name.lower())
                )
                if items:
                    for item in items[:5]:  # Show first 5 items
                        icon = "📁" if item.is_dir() else "📄"
                        content.append(f"{icon} {item.name}")
                    if len(items) > 5:
                        content.append("...")
            except Exception as e:
                content.append(f"[red]Error: {str(e)}[/]")
        else:
            try:
                size = path.stat().st_size
                content.append(f"{size:,} bytes")
                if path.suffix.lower() in {'.txt', '.md', '.py', '.json', '.yaml', '.yml'}:
                    with path.open('r', encoding='utf-8') as f:
                        preview = f.read(200)  # Read first 200 chars
                        if preview.strip():
                            content.append("\n" + preview + ("..." if len(preview) == 200 else ""))
            except Exception as e:
                content.append(f"[red]Error: {str(e)}[/]")
        
        details.update("\n".join(content))

    def action_refresh(self) -> None:
        """Refresh the tree view."""
        self.refresh_tree()

    def action_search(self) -> None:
        """Show search modal."""
        self.push_screen(QuickSearchModal())

    def action_new_item(self) -> None:
        """Create new item dialog."""
        # TODO: Implement new item dialog
        self.notify("New item functionality coming soon!")

    def action_delete(self) -> None:
        """Delete selected item."""
        if self.current_path:
            # TODO: Add confirmation dialog
            self.notify(f"Delete functionality coming soon!")

    def action_move(self) -> None:
        """Move selected item."""
        if self.current_path:
            # TODO: Implement move dialog
            self.notify("Move functionality coming soon!")

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        """Handle tree node selection events."""
        # Just update selection and preview, no auto-opening
        self._process_node_selection(event.node)

    def action_open_selected(self) -> None:
        """Open the selected item in system default application."""
        tree = self.query_one(Tree)
        if not tree.cursor_node or not self.current_path:
            return
            
        # Get the node's label to check if it's a file or folder
        label = str(tree.cursor_node.label)
        is_file = label.startswith("📄")
        
        # For files, make sure we have the correct path
        if is_file:
            # Get the file name without the icon
            file_name = label.split(" ", 1)[1]
            # Make sure we're using the parent directory path
            self.current_path = self.current_path.parent / file_name
            
        # Open the item with system default application
        self.open_with_system_default(self.current_path)

    def open_with_system_default(self, path: Path) -> None:
        """Open a file with the system's default application."""
        print(f"open_with_system_default called with path: {path}")  # Debug print
        try:
            path_str = str(path.resolve())
            print(f"Resolved path: {path_str}")  # Debug print
            self.notify(f"Opening: {path_str}")
            
            if platform.system() == 'Darwin':  # macOS
                print("Using macOS 'open' command")  # Debug print
                result = subprocess.run(['open', path_str], capture_output=True, text=True)
                print(f"Command result: {result}")  # Debug print
                if result.returncode != 0:
                    raise Exception(f"open command failed: {result.stderr}")
            elif platform.system() == 'Windows':
                result = subprocess.run(['start', '', path_str], shell=True, capture_output=True, text=True)
                if result.returncode != 0:
                    raise Exception(f"start command failed: {result.stderr}")
            else:  # Linux and other Unix-like
                result = subprocess.run(['xdg-open', path_str], capture_output=True, text=True)
                if result.returncode != 0:
                    raise Exception(f"xdg-open command failed: {result.stderr}")
            
            self.notify(f"Opened: {path.name}")
        except Exception as e:
            error_msg = f"Error opening {path.name}: {str(e)}"
            print(error_msg)  # Debug print
            self.notify(error_msg, severity="error")

    def on_quick_search_modal_result_action(self, message: QuickSearchModal.ResultAction) -> None:
        """Handle actions from the search modal."""
        if message.action == "select":
            self.select_path(message.path)
        elif message.action == "delete":
            try:
                if message.path.is_dir():
                    shutil.rmtree(message.path)
                else:
                    message.path.unlink()
                self.notify(f"Deleted: {message.path.name}")
                self.refresh_tree()
            except Exception as e:
                self.notify(f"Error deleting {message.path.name}: {e}", severity="error")
        elif message.action.startswith("move:"):
            try:
                new_category = message.action.split(":", 1)[1]
                new_path = DEFAULT_PARA_ROOT / new_category / message.path.name
                if new_path.exists():
                    self.notify(f"Error: {message.path.name} already exists in {new_category}", severity="error")
                    return
                message.path.rename(new_path)
                self.notify(f"Moved: {message.path.name} to {new_category}")
                self.refresh_tree()
            except Exception as e:
                self.notify(f"Error moving {message.path.name}: {e}", severity="error")
        elif message.action == "open":
            self.open_with_system_default(message.path)