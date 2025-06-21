import json
import os

LANG_DIR = "lang"
active_language_data = {}

def load_language(code):
    global active_language_data
    file_path = os.path.join(LANG_DIR, f"{code}.json")
    if not os.path.exists(file_path):
        print(f"⚠️ Language file not found: {file_path}")
        return
    with open(file_path, "r", encoding="utf-8") as f:
        active_language_data = json.load(f)

def get_text(key):
    return active_language_data.get(key, f"[{key}]")

def list_languages():
    langs = []
    for file in os.listdir(LANG_DIR):
        if file.endswith(".json"):
            path = os.path.join(LANG_DIR, file)
            with open(path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    langs.append((file.replace(".json", ""), data.get("lang.name", "Unknown")))
                except:
                    continue
    return langs
