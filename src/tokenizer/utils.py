from pathlib import Path

# A set is used for fast O(1) lookups
BINARY_EXTENSIONS = {
    # Compiled
    ".so", ".o", ".a", ".dll", ".exe",
    # Archives
    ".zip", ".gz", ".tar", ".bz2", ".7z", ".rar", ".ar",
    # Images
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".ico", ".webp",
    # Audio/Video
    ".mp3", ".wav", ".flac", ".ogg", ".mp4", ".avi", ".mov", ".mkv", ".webm",
    # Documents
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
    # Fonts
    ".woff", ".woff2", ".eot", ".ttf", ".otf",
    # Other
    ".bin", ".dat", ".iso", ".img", ".dmg", ".db",
}

def is_binary_path(path: Path) -> bool:
    """Checks if a file path is likely a binary file based on its extension."""
    return path.suffix.lower() in BINARY_EXTENSIONS
