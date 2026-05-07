import sys
import shutil
import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict

from config import EXT_TO_CATEGORY
from utils import handle_duplicate, get_file_age_label

def get_category(filename):
    """Determine category for a file based on extension."""
    ext = Path(filename).suffix.lower()
    if ext in EXT_TO_CATEGORY:
        return EXT_TO_CATEGORY[ext]
    return ("📁 Other", "Other")

def scan_directory(target_dir):
    """Scan directory and categorize all files."""
    target_path = Path(target_dir).expanduser().resolve()
    
    if not target_path.exists():
        print(f"❌ Directory not found: {target_path}")
        sys.exit(1)
    
    results = defaultdict(list)
    skipped = []
    
    for item in sorted(target_path.iterdir()):
        # Skip directories and hidden files
        if item.is_dir():
            skipped.append(str(item.name))
            continue
        if item.name.startswith('.'):
            skipped.append(str(item.name))
            continue
        
        cat_display, cat_folder = get_category(item.name)
        file_size = item.stat().st_size
        modified = datetime.fromtimestamp(item.stat().st_mtime)
        
        results[cat_display].append({
            "name": item.name,
            "path": str(item),
            "category_folder": cat_folder,
            "size": file_size,
            "modified": modified,
            "age_days": (datetime.now() - modified).days,
            "age_label": get_file_age_label(modified)
        })
    
    return results, skipped, target_path

def execute_organization(results, target_path):
    """Actually move files into categorized folders."""
    moved = []
    errors = []
    
    for category, files in results.items():
        for file_info in files:
            src = Path(file_info["path"])
            dest_dir = target_path / file_info["category_folder"]
            dest_dir.mkdir(exist_ok=True)
            
            dest = dest_dir / file_info["name"]
            dest = handle_duplicate(dest)
            
            try:
                shutil.move(str(src), str(dest))
                moved.append({
                    "original": str(src),
                    "destination": str(dest),
                    "category": category
                })
            except Exception as e:
                errors.append({
                    "file": file_info["name"],
                    "error": str(e)
                })
    
    return moved, errors

def save_undo_log(moved, target_path):
    """Save move log for undo functionality."""
    log_path = target_path / ".organizer_undo.json"
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "moves": moved
    }
    with open(log_path, 'w') as f:
        json.dump(log_data, f, indent=2)
    return log_path

def undo_organization(target_dir):
    """Undo the last organization by reading the undo log."""
    target_path = Path(target_dir).expanduser().resolve()
    log_path = target_path / ".organizer_undo.json"
    
    if not log_path.exists():
        print("❌ No undo log found. Nothing to undo.")
        return
    
    with open(log_path) as f:
        log_data = json.load(f)
    
    moves = log_data["moves"]
    restored = 0
    
    for move in moves:
        src = Path(move["destination"])
        dest = Path(move["original"])
        
        if src.exists():
            shutil.move(str(src), str(dest))
            restored += 1
    
    # Clean up empty category folders
    for item in target_path.iterdir():
        if item.is_dir() and not any(item.iterdir()):
            item.rmdir()
    
    log_path.unlink()
    print(f"✅ Restored {restored}/{len(moves)} files to original locations.")
