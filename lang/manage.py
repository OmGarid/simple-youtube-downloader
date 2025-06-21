# lang/manage.py
from config import load_config, save_config

def set_language(lang_code):
    config = load_config()
    config["language"] = lang_code
    save_config(config)
