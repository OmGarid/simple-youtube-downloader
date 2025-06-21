import json
import os

active_language_data = {}
language_directory = os.path.join(os.path.dirname(__file__))

def load_language(lang_code: str):
    """
    Load language JSON file based on lang_code (e.g. 'en_us')
    """
    global active_language_data
    file_path = os.path.join(language_directory, f"{lang_code}.json")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            active_language_data = json.load(f)
    except Exception as e:
        print(f"⚠️ Failed to load language '{lang_code}': {e}")
        active_language_data = {}

def get_text(key: str) -> str:
    """
    Get the translated text from loaded language data.
    If key not found, returns [key].
    """
    return active_language_data.get(key, f"[{key}]")

def get_available_languages():
    """
    Scan /lang/ directory and return list of tuples:
    [(language_code, full_name_from_json), ...]
    """
    langs = []
    for filename in os.listdir(language_directory):
        if filename.endswith(".json") and filename != "identifier.json":
            code = filename[:-5]
            path = os.path.join(language_directory, filename)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    name = data.get("lang.name", code)
                    langs.append((code, name))
            except:
                continue
    return langs
