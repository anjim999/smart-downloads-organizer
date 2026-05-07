from utils import format_size

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    Console = None
    RICH_AVAILABLE = False

def display_results_rich(results, skipped, target_path, dry_run=True):
    """Display results using rich library."""
    console = Console()
    
    # Header
    mode = "🔍 DRY RUN (Preview)" if dry_run else "🚀 EXECUTING"
    console.print()
    console.print(Panel(
        f"[bold cyan]Smart Downloads Organizer[/]\n"
        f"[dim]Target: {target_path}[/]\n"
        f"[{'yellow' if dry_run else 'green'}]{mode}[/]",
        box=box.DOUBLE,
        border_style="cyan"
    ))
    console.print()
    
    # Summary table
    table = Table(
        title="📋 File Organization Plan",
        box=box.ROUNDED,
        show_lines=True,
        title_style="bold white",
        border_style="bright_blue"
    )
    table.add_column("Category", style="bold", min_width=18)
    table.add_column("Files", justify="center", style="cyan", min_width=8)
    table.add_column("Total Size", justify="right", style="green", min_width=12)
    table.add_column("Sample Files", style="dim", max_width=50)
    
    total_files = 0
    total_size = 0
    
    for category in sorted(results.keys()):
        files = results[category]
        count = len(files)
        size = sum(f["size"] for f in files)
        total_files += count
        total_size += size
        
        # Show first 3 file names as samples
        samples = ", ".join(f["name"][:30] for f in files[:3])
        if count > 3:
            samples += f" (+{count - 3} more)"
        
        table.add_row(
            category,
            str(count),
            format_size(size),
            samples
        )
    
    table.add_row(
        "[bold]TOTAL[/]",
        f"[bold]{total_files}[/]",
        f"[bold]{format_size(total_size)}[/]",
        "",
        style="on grey23"
    )
    
    console.print(table)
    console.print()
    
    # Skipped items
    if skipped:
        skip_text = ", ".join(skipped[:5])
        if len(skipped) > 5:
            skip_text += f" (+{len(skipped) - 5} more)"
        console.print(f"[dim]⏭️  Skipped {len(skipped)} items (directories/hidden): {skip_text}[/]")
        console.print()
    
    return total_files, total_size

def display_results_plain(results, skipped, target_path, dry_run=True):
    """Display results without rich (plain text fallback)."""
    mode = "DRY RUN (Preview)" if dry_run else "EXECUTING"
    print(f"\n{'='*60}")
    print(f"  Smart Downloads Organizer")
    print(f"  Target: {target_path}")
    print(f"  Mode: {mode}")
    print(f"{'='*60}\n")
    
    total_files = 0
    total_size = 0
    
    print(f"{'Category':<20} {'Files':>6} {'Size':>12}  Sample Files")
    print(f"{'-'*20} {'-'*6} {'-'*12}  {'-'*30}")
    
    for category in sorted(results.keys()):
        files = results[category]
        count = len(files)
        size = sum(f["size"] for f in files)
        total_files += count
        total_size += size
        
        samples = ", ".join(f["name"][:25] for f in files[:2])
        if count > 2:
            samples += f" (+{count - 2})"
        
        print(f"{category:<20} {count:>6} {format_size(size):>12}  {samples}")
    
    print(f"{'-'*20} {'-'*6} {'-'*12}")
    print(f"{'TOTAL':<20} {total_files:>6} {format_size(total_size):>12}")
    print()
    
    return total_files, total_size

def show_stats(results):
    """Show file age statistics."""
    all_files = []
    for files in results.values():
        all_files.extend(files)
    
    if not all_files:
        return
    
    today = 0
    this_week = 0
    this_month = 0
    older = 0
    
    for f in all_files:
        age = f["age_days"]
        if age == 0:
            today += 1
        elif age < 7:
            this_week += 1
        elif age < 30:
            this_month += 1
        else:
            older += 1
    
    if RICH_AVAILABLE:
        console = Console()
        console.print()
        console.print(Panel(
            f"[green]Today: {today}[/] | [cyan]This week: {this_week}[/] | "
            f"[yellow]This month: {this_month}[/] | [red]Older: {older}[/]",
            title="📊 File Age Stats",
            border_style="magenta"
        ))
    else:
        print(f"\n📊 File Age: Today={today} | Week={this_week} | Month={this_month} | Older={older}")
