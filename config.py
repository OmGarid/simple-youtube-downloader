import json
import os

CONFIG_FILE = "config.json"
DEFAULT_CONFIG = {
    "language": "en_us",
    "output_path": "",
    "audio_only": False,
    "advanced": {
        "enabled": False,
        "proxy": "",
        "cookies": "",
        "user_agent": "",
        "headers": ""
    }
}

def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

def set_language(lang_code):
    config = load_config()
    config["language"] = lang_code
    save_config(config)

def update_advanced_options(options):
    config = load_config()
    config["advanced"].update(options)
    save_config(config)
