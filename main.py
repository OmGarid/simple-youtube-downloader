from bootstrap import bootstrap
from config import load_config
from gui import launch_gui

if __name__ == "__main__":
    bootstrap()
    config = load_config()
    launch_gui(config)
