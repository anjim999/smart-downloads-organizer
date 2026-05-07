#!/usr/bin/env python3
"""
Smart Downloads Organizer
=========================
Automatically organizes messy Downloads folder into categorized subfolders.
Handles duplicates, shows a beautiful summary, and supports dry-run mode.
"""

import argparse
from pathlib import Path
import shutil
from core import scan_directory, execute_organization, save_undo_log, undo_organization
from display import display_results_rich, display_results_plain, show_stats, RICH_AVAILABLE

try:
    from rich.console import Console
except ImportError:
    Console = None

def main():
    parser = argparse.ArgumentParser(
        description="🗂️ Smart Downloads Organizer - Automatically organize your messy Downloads folder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python organize.py                     # Preview what would happen
  python organize.py --execute           # Actually organize files
  python organize.py --watch             # Watch for new files in background
  python organize.py --reset             # Hard reset: move all files out of folders
  python organize.py --path ~/Downloads  # Specify custom path
  python organize.py --undo              # Undo last organization
        """
    )
    parser.add_argument("--path", default="~/Downloads", help="Directory to organize (default: ~/Downloads)")
    parser.add_argument("--execute", action="store_true", help="Actually move files (default is dry-run)")
    parser.add_argument("--watch", action="store_true", help="Run continuously in background and auto-organize new files")
    parser.add_argument("--reset", action="store_true", help="Hard reset: pull all files out of category folders")
    parser.add_argument("--undo", action="store_true", help="Undo the last organization")
    parser.add_argument("--stats", action="store_true", help="Show file age statistics")
    
    args = parser.parse_args()
    
    # Handle hard reset (New Feature!)
    if args.reset:
        target = Path(args.path).expanduser()
        restored = 0
        categories = ["Documents", "Images", "Videos", "Audio", "Archives", "Code", "Spreadsheets", "Email", "Installers", "Other", "sd"]
        for folder in target.iterdir():
            if folder.is_dir() and folder.name in categories:
                # Yank EVERYTHING out (files, sub-folders, hidden files)
                for item in folder.iterdir():
                    dest = target / item.name
                    counter = 1
                    while dest.exists():
                        dest = target / f"{item.stem} ({counter}){item.suffix}"
                        counter += 1
                    shutil.move(str(item), str(dest))
                    restored += 1
                
                # Forcefully destroy the now-empty folder
                try:
                    shutil.rmtree(str(folder))
                except Exception:
                    pass
                    
        print(f"✅ HARD RESET: Pulled {restored} items back to the main folder and destroyed category folders!")
        return


    # Handle undo
    if args.undo:
        undo_organization(args.path)
        return
        
    # Handle watch
    if args.watch:
        try:
            from watcher import start_watching
            start_watching(args.path)
        except ImportError:
            print("❌ Watch mode requires 'watchdog'. Run: pip install watchdog")
        return
    
    # Scan and categorize
    results, skipped, target_path = scan_directory(args.path)
    
    if not results:
        print("✨ Directory is already clean! No files to organize.")
        return
    
    # Show stats if requested
    if args.stats:
        show_stats(results)
    
    # Display results
    dry_run = not args.execute
    if RICH_AVAILABLE:
        total_files, total_size = display_results_rich(results, skipped, target_path, dry_run)
    else:
        total_files, total_size = display_results_plain(results, skipped, target_path, dry_run)
    
    # Execute if not dry run
    if args.execute:
        moved, errors = execute_organization(results, target_path)
        
        # Save undo log
        if moved:
            log_path = save_undo_log(moved, target_path)
        
        if RICH_AVAILABLE and Console:
            console = Console()
            console.print(f"[bold green]✅ Organized {len(moved)} files into {len(set(m['category'] for m in moved))} categories![/]")
            if errors:
                console.print(f"[bold red]⚠️  {len(errors)} errors occurred[/]")
                for err in errors:
                    console.print(f"[red]  - {err['file']}: {err['error']}[/]")
            console.print(f"[dim]💾 Undo log saved. Run with --undo to reverse.[/]")
        else:
            print(f"✅ Organized {len(moved)} files!")
            if errors:
                print(f"⚠️  {len(errors)} errors:")
                for err in errors:
                    print(f"  - {err['file']}: {err['error']}")
            print(f"💾 Undo log saved. Run with --undo to reverse.")
    else:
        if RICH_AVAILABLE and Console:
            console = Console()
            console.print("[yellow]👆 This was a dry run. Add [bold]--execute[/bold] to actually organize files.[/]")
        else:
            print("👆 This was a dry run. Add --execute to actually organize files.")

if __name__ == "__main__":
    main()
