import json
import os
from datetime import datetime

HISTORY_FILE = "command.history.json"
MAX_HISTORY_ENTRIES = 50

def load_history():
    """Load command history from the JSON file."""
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)

def save_history(history):
    """Save a trimmed version of the history to the file."""
    with open(HISTORY_FILE, "w") as f:
        json.dump(history[-MAX_HISTORY_ENTRIES:], f, indent=2)

def add_to_history(filename, mode, connection_info):
    """Add a new command entry to history."""
    history = load_history()
    entry = {
        "filename": filename,
        "timestamp": datetime.now().isoformat(timespec='seconds'),
        "mode": mode,
        "connection": connection_info
    }
    history.append(entry)
    save_history(history)

def display_history():
    """Print recent command history to the console."""
    history = load_history()
    if not history:
        print("📭 No command history yet.")
        return
    print("🕘 Recent Commands:")
    for i, entry in enumerate(reversed(history), 1):
        conn = ", ".join(f"{k}={v}" for k, v in entry.get("connection", {}).items())
        print(f"{i}. {entry['filename']} | {entry['timestamp']} | {entry['mode']} | {conn}")

def get_history_entry(index_from_latest):
    """
    Get a command entry by its index from latest shown.
    index_from_latest = 0 is most recent.
    """
    history = load_history()
    if 0 <= index_from_latest < len(history):
        return history[-(index_from_latest + 1)]  # Reverse indexing
    return None
