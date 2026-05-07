CATEGORIES = {
    "📄 Documents": {
        "extensions": [".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf", ".md", ".tex"],
        "folder": "Documents"
    },
    "🖼️ Images": {
        "extensions": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg", ".webp", ".ico", ".tiff", ".jfif", ".avif", ".heic"],
        "folder": "Images"
    },
    "🎥 Videos": {
        "extensions": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"],
        "folder": "Videos"
    },
    "🎵 Audio": {
        "extensions": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma"],
        "folder": "Audio"
    },
    "📦 Archives": {
        "extensions": [".zip", ".tar", ".gz", ".rar", ".7z", ".bz2", ".xz", ".deb", ".rpm"],
        "folder": "Archives"
    },
    "💻 Code": {
        "extensions": [".py", ".js", ".ts", ".jsx", ".tsx", ".html", ".css", ".java",
                       ".cpp", ".c", ".go", ".rs", ".rb", ".php", ".sh", ".json", ".yml",
                       ".yaml", ".xml", ".sql", ".ipynb"],
        "folder": "Code"
    },
    "📊 Spreadsheets": {
        "extensions": [".csv", ".xls", ".xlsx", ".ods"],
        "folder": "Spreadsheets"
    },
    "📧 Email": {
        "extensions": [".eml", ".msg"],
        "folder": "Email"
    },
    "🔧 Installers": {
        "extensions": [".exe", ".msi", ".dmg", ".appimage", ".snap", ".flatpak"],
        "folder": "Installers"
    }
}

# Build reverse lookup: extension -> category
EXT_TO_CATEGORY = {}
for cat_name, cat_info in CATEGORIES.items():
    for ext in cat_info["extensions"]:
        EXT_TO_CATEGORY[ext] = (cat_name, cat_info["folder"])
