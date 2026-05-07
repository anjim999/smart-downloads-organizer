from datetime import datetime

def handle_duplicate(dest_path):
    """Generate a unique filename if destination already exists."""
    if not dest_path.exists():
        return dest_path
    
    stem = dest_path.stem
    suffix = dest_path.suffix
    parent = dest_path.parent
    counter = 1
    
    while True:
        new_name = f"{stem} ({counter}){suffix}"
        new_path = parent / new_name
        if not new_path.exists():
            return new_path
        counter += 1

def get_file_age_label(modified_date):
    """Return a human-readable age label for a file."""
    age_days = (datetime.now() - modified_date).days
    if age_days == 0:
        return "today"
    elif age_days == 1:
        return "yesterday"
    elif age_days < 7:
        return f"{age_days}d ago"
    elif age_days < 30:
        weeks = age_days // 7
        return f"{weeks}w ago"
    elif age_days < 365:
        months = age_days // 30
        return f"{months}mo ago"
    else:
        years = age_days // 365
        return f"{years}y ago"

def format_size(size_bytes):
    """Convert bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"
