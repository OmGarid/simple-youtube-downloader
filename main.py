from gui import launch_gui
from config import load_config, save_config, set_language
from lang import get_text, load_language

if __name__ == "__main__":
    config = load_config()
    load_language(config["language"])
    launch_gui(config)
