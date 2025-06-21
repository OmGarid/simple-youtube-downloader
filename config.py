import json
import os

CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "language": "en_us",
        "output_dir": os.getcwd(),
        "audio_only": False
    }

def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

def set_language(lang_code):
    config = load_config()
    config["language"] = lang_code
    save_config(config)
