import json
import os

META_FILE = "command.meta.json"

DEFAULT_META = {
    "delay": 0.2,
    "mode": "UDP",
    "parser": "HEX"
}

def load_meta():
    if not os.path.exists(META_FILE):
        save_meta(DEFAULT_META)
    with open(META_FILE, "r") as f:
        return json.load(f)

def save_meta(data):
    with open(META_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_delay():
    return load_meta().get("delay", DEFAULT_META["delay"])

def save_delay(delay):
    meta = load_meta()
    meta["delay"] = delay
    save_meta(meta)
