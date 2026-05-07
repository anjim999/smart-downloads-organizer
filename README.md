# 🗂️ Smart Downloads Organizer

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)
![Systemd](https://img.shields.io/badge/Daemon-systemd-brightgreen.svg)

A production-ready Python CLI tool and background daemon that automatically organizes a messy Downloads folder into categorized subfolders with duplicate-handling and an undo safety net.

## ✨ Features
* **Auto-Categorization:** Scans files and moves them into predefined folders (`Documents`, `Images`, `Videos`, `Code`, `Archives`, etc.) based on their extension.
* **Real-time Watcher:** Runs continuously in the background using `watchdog`. The exact second a file finishes downloading, it instantly routes it to the right folder.
* **Linux Systemd Daemon:** Includes an installation script to register the tool as a Linux service so it boots invisibly with your OS.
* **Duplicate Handling:** Automatically appends counters (e.g., `resume (1).pdf`) if a file with the same name already exists in the destination.
* **Undo System:** Saves a JSON log of every move. Made a mistake? Run `--undo` to instantly restore all files to their original location.
* **Modular Architecture:** Cleanly separated code (`core.py`, `utils.py`, `display.py`, `watcher.py`) making it easy to extend or write tests.
* **Beautiful CLI:** Uses `rich` for stunning terminal tables, stats, and colored output.

## 🚀 Quick Start (Manual Mode)

If you just want to run the tool once to clean up a messy folder:

```bash
# 1. Install dependencies
pip install watchdog rich

# 2. Preview what would happen (Dry Run)
python organize.py

# 3. Actually organize files
python organize.py --execute

# 4. View statistics about file age
python organize.py --stats

# 5. Undo the last cleanup (if needed)
python organize.py --undo
```

## ⚙️ Real-World Automation (Background Daemon)

Real developers don't run scripts manually. Install this as a background service so you literally never have to think about sorting files again.

### Installation (Linux)
Run the included bash script to register the watcher as a `systemd` daemon:
```bash
chmod +x install_service.sh
./install_service.sh
```

### Management
Once installed, your OS will run it automatically on startup. To manage the daemon:
```bash
systemctl --user status smart-organizer  # Check if it's running
systemctl --user stop smart-organizer    # Stop the service
journalctl --user -u smart-organizer -f  # View real-time logs
```

## 📂 Category Map
| Category | Extensions |
|----------|-----------|
| 📄 Documents | `.pdf`, `.doc`, `.docx`, `.txt`, `.md`, `.rtf`, `.tex` |
| 🖼️ Images | `.png`, `.jpg`, `.jpeg`, `.gif`, `.svg`, `.webp`, `.ico` |
| 🎥 Videos | `.mp4`, `.mkv`, `.avi`, `.webm`, `.mov`, `.flv` |
| 🎵 Audio | `.mp3`, `.wav`, `.flac`, `.aac`, `.m4a` |
| 📦 Archives | `.zip`, `.tar`, `.gz`, `.deb`, `.rar`, `.7z` |
| 💻 Code | `.py`, `.js`, `.ts`, `.json`, `.html`, `.css`, `.cpp`, `.sql` |
| 📊 Spreadsheets| `.csv`, `.xls`, `.xlsx`, `.ods` |
| 🔧 Installers | `.exe`, `.dmg`, `.appimage`, `.snap` |

## 🛠️ Architecture
The monolithic logic was structurally refactored into a scalable design:
- `organize.py` - Main CLI entrypoint and argument parser.
- `core.py` - Core execution logic for scanning, moving, and undoing.
- `watcher.py` - FileSystem event handlers bridging `watchdog` to the core logic.
- `utils.py` - Helpers for duplicate resolution, file sizing, and date logic.
- `display.py` - Rich terminal UI rendering and fallback printing.
- `config.py` - Configuration maps linking extensions to categories.

## 📝 License
MIT License - Feel free to fork and modify!
