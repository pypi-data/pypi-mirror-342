"""
PARA CLI - Main command line interface.
"""
from pathlib import Path
from typing import Optional, Tuple, List
import fnmatch

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.tree import Tree

app = typer.Typer(
    name="para",
    help="A command line tool for managing your PARA system.",
    add_completion=False,
)
console = Console()

# Default PARA root directory in the user's Documents folder
DEFAULT_PARA_ROOT = Path("~/Documents/PARA").expanduser()

# PARA categories with numbered prefixes
CATEGORIES = [
    "00 Inbox",
    "01 Projects",
    "02 Areas",
    "03 Resources",
    "04 Archives"
]

def get_visible_items(path: Path) -> Tuple[int, int]:
    """Get count of visible folders and files (excluding hidden ones)."""
    items = [item for item in path.iterdir() if not item.name.startswith('.')]
    folders = sum(1 for item in items if item.is_dir())
    files = sum(1 for item in items if item.is_file())
    return folders, files

def get_category_from_input(category: str) -> Optional[str]:
    """Convert user input category to actual category name."""
    category = category.lower()
    mapping = {
        "inbox": "00 Inbox",
        "projects": "01 Projects",
        "areas": "02 Areas",
        "resources": "03 Resources",
        "archives": "04 Archives",
        "archive": "04 Archives",
    }
    return mapping.get(category)

def is_para_initialized(path: Path) -> bool:
    """Check if PARA structure exists at the given path."""
    if not path.exists():
        return False
    return all((path / category).exists() for category in CATEGORIES)

def ensure_para_structure():
    """Ensure the PARA directory structure exists."""
    for category in CATEGORIES:
        category_path = DEFAULT_PARA_ROOT / category
        category_path.mkdir(parents=True, exist_ok=True)

def search_in_directory(path: Path, query: str) -> List[Path]:
    """Search for items matching the query in the given directory."""
    results = []
    if not path.exists():
        return results

    for item in path.rglob("*"):
        if item.is_file() or item.is_dir():
            if fnmatch.fnmatch(item.name.lower(), f"*{query.lower()}*"):
                results.append(item)
    return results

@app.callback(invoke_without_command=True)
def callback(ctx: typer.Context):
    """
    PARA CLI - Manage your personal knowledge management system using the PARA method.
    """
    if ctx.invoked_subcommand is None:
        # Show welcome message and help
        welcome_text = Text()
        welcome_text.append("Welcome to ", style="bold cyan")
        welcome_text.append("PARA CLI", style="bold green")
        welcome_text.append("!", style="bold cyan")
        console.print(Panel(welcome_text, expand=False))
        
        console.print("\n[bold]Available Commands:[/]")
        commands_table = Table(show_header=False, box=None)
        commands_table.add_row("[bold cyan]init[/]", "Initialize PARA directory structure")
        commands_table.add_row("[bold cyan]ls[/]", "List PARA system contents")
        commands_table.add_row("[bold cyan]add[/]", "Add new item to a PARA category")
        commands_table.add_row("[bold cyan]search[/]", "Search through PARA system")
        commands_table.add_row("[bold cyan]/i[/]", "Launch interactive TUI mode")
        console.print(commands_table)
        
        console.print("\n[bold]Examples:[/]")
        examples_table = Table(show_header=False, box=None)
        examples_table.add_row("[dim]$[/] [green]para init[/]", "Create PARA structure")
        examples_table.add_row("[dim]$[/] [green]para init --path ~/custom/para[/]", "Create in custom location")
        examples_table.add_row("[dim]$[/] [green]para ls[/]", "List all categories")
        examples_table.add_row("[dim]$[/] [green]para ls --tree[/]", "Show tree view")
        examples_table.add_row("[dim]$[/] [green]para add \"New Project\" projects[/]", "Add a new project")
        examples_table.add_row("[dim]$[/] [green]para search \"python\"[/]", "Search everywhere")
        examples_table.add_row("[dim]$[/] [green]para search \"book\" -r[/]", "Search in Resources")
        examples_table.add_row("[dim]$[/] [green]para search \"2024\" -p -a[/]", "Search in Projects and Areas")
        examples_table.add_row("[dim]$[/] [green]para /i[/]", "Launch TUI mode")
        console.print(examples_table)
        
        console.print("\nFor more details on a command, run: [bold cyan]para COMMAND --help[/]")

@app.command()
def init(
    path: Optional[Path] = typer.Option(
        None,
        "--path",
        "-p",
        help="Custom path for PARA root directory",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Force re-initialization even if PARA structure exists",
    )
):
    """Initialize the PARA directory structure."""
    para_root = path or DEFAULT_PARA_ROOT
    
    if is_para_initialized(para_root) and not force:
        console.print(f"[yellow]⚠️  PARA system already exists at: {para_root}[/]")
        console.print("[yellow]Use --force to reinitialize if needed.[/]")
        return

    try:
        for category in CATEGORIES:
            category_path = para_root / category
            category_path.mkdir(parents=True, exist_ok=True)
        console.print(f"✨ PARA system {'reinitialized' if force else 'initialized'} at: [bold green]{para_root}[/]")
    except Exception as e:
        console.print(f"[bold red]Error:[/] Failed to initialize PARA system: {str(e)}")

@app.command(name="ls")
def list_contents(
    tree: bool = typer.Option(
        False,
        "--tree",
        "-t",
        help="Show detailed tree view of the PARA structure",
    )
):
    """List PARA system contents."""
    if not DEFAULT_PARA_ROOT.exists():
        console.print("[bold red]Error:[/] PARA system not initialized. Run 'para init' first.")
        return

    if tree:
        # Show tree view
        root = Tree(f"[bold]PARA[/] [dim]{DEFAULT_PARA_ROOT}[/]")
        for category in CATEGORIES:
            category_path = DEFAULT_PARA_ROOT / category
            if category_path.exists():
                folders, files = get_visible_items(category_path)
                cat_tree = root.add(f"[cyan]{category}[/] [dim]({folders} folders, {files} files)[/]")
                items = [item for item in category_path.iterdir() if not item.name.startswith('.')]
                for item in sorted(items):
                    if item.is_dir():
                        cat_tree.add(f"[green]📁 {item.name}[/]")
                    else:
                        cat_tree.add(f"[yellow]📄 {item.name}[/]")
        console.print(root)
        return

    # Show table view
    table = Table(title="PARA System Contents")
    table.add_column("Category", style="cyan")
    table.add_column("Folders", style="green", justify="right")
    table.add_column("Files", style="yellow", justify="right")
    table.add_column("Path", style="blue")

    for category in CATEGORIES:
        category_path = DEFAULT_PARA_ROOT / category
        if category_path.exists():
            folders, files = get_visible_items(category_path)
            table.add_row(
                category,
                str(folders),
                str(files),
                str(category_path)
            )

    console.print(table)

@app.command()
def add(
    name: str = typer.Argument(..., help="Name of the item to add"),
    category: str = typer.Argument(..., help="Category to add the item to (inbox/projects/areas/resources/archives)"),
):
    """Add a new item to a PARA category."""
    actual_category = get_category_from_input(category)
    if actual_category is None:
        console.print(f"[bold red]Error:[/] Invalid category. Must be one of: inbox, projects, areas, resources, archives")
        return

    try:
        ensure_para_structure()
        item_path = DEFAULT_PARA_ROOT / actual_category / name
        item_path.mkdir(parents=True, exist_ok=True)
        console.print(f"✨ Created [bold green]{name}[/] in [bold blue]{actual_category}[/]")
    except Exception as e:
        console.print(f"[bold red]Error:[/] Failed to create item: {str(e)}")

@app.command()
def search(
    query: str = typer.Argument(..., help="Search query"),
    inbox: bool = typer.Option(False, "-i", help="Search only in Inbox"),
    projects: bool = typer.Option(False, "-p", help="Search only in Projects"),
    areas: bool = typer.Option(False, "-a", help="Search only in Areas"),
    resources: bool = typer.Option(False, "-r", help="Search only in Resources"),
    archives: bool = typer.Option(False, "-x", help="Search only in Archives"),
    relative: bool = typer.Option(False, "--relative", "-l", help="Show relative paths instead of full paths"),
):
    """
    Search through PARA system. 
    If no category flag is specified, searches everywhere.
    """
    if not DEFAULT_PARA_ROOT.exists():
        console.print("[bold red]Error:[/] PARA system not initialized. Run 'para init' first.")
        return

    # If no flags are set, search in all categories
    search_all = not any([inbox, projects, areas, resources, archives])
    
    # Map categories to their flags
    category_flags = {
        "00 Inbox": inbox,
        "01 Projects": projects,
        "02 Areas": areas,
        "03 Resources": resources,
        "04 Archives": archives
    }

    results_table = Table(title=f"Search Results for: [bold cyan]{query}[/]")
    results_table.add_column("Category", style="cyan")
    results_table.add_column("Type", style="yellow")
    results_table.add_column("Name", style="green")
    results_table.add_column("Path", style="blue")

    total_results = 0

    for category in CATEGORIES:
        if search_all or category_flags[category]:
            category_path = DEFAULT_PARA_ROOT / category
            results = search_in_directory(category_path, query)
            
            for item in sorted(results):
                try:
                    item_type = "📁 Dir" if item.is_dir() else "📄 File"
                    
                    if relative:
                        # Show path relative to category
                        rel_path = item.relative_to(category_path)
                        display_path = str(rel_path.parent if rel_path.parent != Path(".") else "")
                    else:
                        # Show full absolute path that will be clickable
                        display_path = str(item.resolve())
                    
                    results_table.add_row(
                        category,
                        item_type,
                        item.name,
                        display_path
                    )
                    total_results += 1
                except Exception as e:
                    console.print(f"[red]Error processing path: {item}[/]")

    if total_results > 0:
        console.print(results_table)
        console.print(f"\nFound [bold green]{total_results}[/] matching items")
        if not relative:
            console.print("[dim]Tip: Use --relative or -l to show shorter relative paths[/]")
    else:
        console.print(f"[yellow]No matches found for: [bold]{query}[/][/]")

@app.command(name="/i")
@app.command(name="interactive")
def interactive_mode():
    """
    Launch interactive TUI mode.
    Navigate and manage your PARA system using a terminal user interface.
    """
    try:
        from .interactive import ParaApp
    except ImportError:
        console.print("[bold red]Error:[/] Interactive mode requires additional dependencies.")
        console.print("Please install them with: [bold cyan]pip install textual[/]")
        return

    if not DEFAULT_PARA_ROOT.exists():
        console.print("[bold red]Error:[/] PARA system not initialized. Run 'para init' first.")
        return

    app = ParaApp()
    app.run()

def main():
    """Main entry point for the CLI."""
    app() 