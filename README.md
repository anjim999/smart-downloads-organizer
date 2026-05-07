# 🗂️ Smart Downloads Organizer

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)
![Systemd](https://img.shields.io/badge/Daemon-systemd-brightgreen.svg)

A production-ready Python CLI tool and background daemon that automatically organizes a messy Downloads folder into categorized subfolders. It features real-time background watching, intelligent duplicate-handling, an undo safety net, and a "hard reset" capability.

## ✨ Core Features
* **Real-time Background Watcher:** Uses the `watchdog` library to listen to OS-level file events. The exact second a file finishes downloading, it instantly routes it to the right folder without you lifting a finger.
* **Auto-Categorization:** Automatically scans and moves files into predefined folders (`Documents`, `Images`, `Videos`, `Code`, etc.) based on their extension.
* **Linux Systemd Daemon:** Includes an installation bash script (`install_service.sh`) to register the tool as a system-level Linux service so it boots invisibly with your OS.
* **Undo System:** Saves a JSON log of every manual move. Made a mistake? Run `--undo` to parse the log and restore all files to their original location.
* **Hard Reset Capability:** A `--reset` flag that forcefully yanks every file and sub-folder back out of the category folders and restores them to the main directory, destroying the empty folders behind it.
* **Modular Architecture:** Cleanly separated code (`core.py`, `utils.py`, `display.py`, `watcher.py`) adhering to clean code principles, making it easy to test and extend.

## 🚀 Usage Guide

There are **three** different ways you can use this automation:

### 1. Fully Automated (Best for the future)
Instead of running it manually every week, turn it on as a background service. It will quietly run forever and instantly organize any NEW files you download.
```bash
# Install it as a system service
chmod +x install_service.sh
./install_service.sh

# To check if it is actively running in the background:
systemctl --user status smart-organizer
```

### 2. Manual Cleanup (Best for existing messes)
If you already have a messy folder with 100+ files, the watcher won't touch them (it only looks for new files). You must run the execute command once to clean up the past.
```bash
# Preview what it will do before touching any data (Dry Run)
python3 organize.py

# Actually organize all existing files right now
python3 organize.py --execute

# Generate statistical metrics on file ages
python3 organize.py --stats
```

### 3. Reverting the Changes
If you decide you don't like the grouped folders and want all your files back exactly how they were, you have two options:
```bash
# Option A: Soft Undo (Reads the JSON log to reverse the exact last operation)
python3 organize.py --undo

# Option B: Hard Reset (Forcefully pulls all files back into the main folder and deletes category folders)
python3 organize.py --reset
```

## 📂 Category Mappings
| Category | Supported Extensions |
|----------|-----------|
| 📄 Documents | `.pdf`, `.doc`, `.docx`, `.txt`, `.md`, `.rtf`, `.tex` |
| 🖼️ Images | `.png`, `.jpg`, `.jpeg`, `.gif`, `.svg`, `.webp`, `.ico`, `.jfif`, `.avif`, `.heic` |
| 🎥 Videos | `.mp4`, `.mkv`, `.avi`, `.webm`, `.mov`, `.flv` |
| 🎵 Audio | `.mp3`, `.wav`, `.flac`, `.aac`, `.m4a` |
| 📦 Archives | `.zip`, `.tar`, `.gz`, `.deb`, `.rar`, `.7z` |
| 💻 Code | `.py`, `.js`, `.ts`, `.json`, `.html`, `.css`, `.cpp`, `.sql` |
| 📊 Spreadsheets| `.csv`, `.xls`, `.xlsx`, `.ods` |
| 🔧 Installers | `.exe`, `.dmg`, `.appimage`, `.snap` |

## 🛠️ System Architecture
The monolithic logic was structurally refactored into a scalable, multi-file design:
- `organize.py` - Main CLI entrypoint and argument parser.
- `core.py` - Core execution logic for scanning, moving, and undoing.
- `watcher.py` - FileSystem event handlers bridging `watchdog` to the core logic.
- `utils.py` - Helpers for duplicate resolution, file sizing, and date logic.
- `display.py` - Rich terminal UI rendering and fallback printing.
- `config.py` - Configuration maps linking extensions to categories.

## 📝 License
MIT License - Open Source Software.