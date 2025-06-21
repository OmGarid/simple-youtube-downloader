import json
import os

LANG_DIR = "lang"
IDENTIFIER_FILE = os.path.join(LANG_DIR, "identifier.json")

active_language_code = "en_us"
active_language_data = {}

def set_active_language(code):
    global active_language_code, active_language_data
    file_path = os.path.join(LANG_DIR, f"{code}.json")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            active_language_data = json.load(f)
            active_language_code = code
    except Exception as e:
        print(f"⚠️ Failed to load language '{code}': {e}")
        active_language_data = {}

def get_text(key):
    global active_language_data
    return active_language_data.get(key, key)

def list_languages():
    try:
        with open(IDENTIFIER_FILE, "r", encoding="utf-8") as f:
            identifiers = json.load(f)
            keys = list(identifiers.keys())
            names = list(identifiers.values())
            return keys, names
    except Exception as e:
        print(f"⚠️ Failed to read identifier file: {e}")
        return ["en_us"], ["English-US"]
