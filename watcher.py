import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from core import get_category
from utils import handle_duplicate
import shutil

class DownloadOrganizerHandler(FileSystemEventHandler):
    def __init__(self, target_path):
        self.target_path = Path(target_path).resolve()
        
    def on_created(self, event):
        if event.is_directory:
            return
            
        file_path = Path(event.src_path)
        
        # Skip hidden files or temp download files (.crdownload, .part)
        if file_path.name.startswith('.') or file_path.suffix in ['.crdownload', '.part', '.tmp']:
            return
            
        # Wait slightly to ensure file is completely written by the OS/Browser
        time.sleep(2)
        
        if not file_path.exists():
            return
            
        cat_display, cat_folder = get_category(file_path.name)
        
        dest_dir = self.target_path / cat_folder
        dest_dir.mkdir(exist_ok=True)
        
        dest = dest_dir / file_path.name
        dest = handle_duplicate(dest)
        
        try:
            shutil.move(str(file_path), str(dest))
            print(f"🤖 Auto-organized: {file_path.name} -> {cat_folder}/")
        except Exception as e:
            print(f"⚠️ Error moving {file_path.name}: {e}")

def start_watching(target_dir):
    target_path = Path(target_dir).expanduser().resolve()
    
    if not target_path.exists():
        print(f"❌ Directory not found: {target_path}")
        return

    event_handler = DownloadOrganizerHandler(target_path)
    observer = Observer()
    observer.schedule(event_handler, str(target_path), recursive=False)
    observer.start()
    
    print(f"👀 Watching {target_path} for new files... (Press Ctrl+C to stop)")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n🛑 Stopped watching.")
    observer.join()
