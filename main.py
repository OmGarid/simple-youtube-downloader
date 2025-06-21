from gui import launch_gui
from config import load_config, save_config, set_language
from lang import get_text, load_language

DEFAULT_ADVANCED = {
    "enabled": False,
    "proxy": "",
    "cookies": "",
    "user_agent": "",
    "headers": ""
}

if __name__ == "__main__":
    config = load_config()
    
    # ✅ Tambahkan bagian ini:
    if "advanced" not in config:
        config["advanced"] = DEFAULT_ADVANCED
        save_config(config)

    load_language(config["language"])
    launch_gui(config)
