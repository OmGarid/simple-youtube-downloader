
import os
import sys
import json
import threading
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import platform
import subprocess
import importlib.util
import urllib.request
import zipfile
import shutil

# ================== BOOTSTRAP ==================
REQUIRED_MODULES = ["yt_dlp", "tkinter"]
FFMPEG_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
FFMPEG_DIR = "ffmpeg"

def check_and_install():
    for module in REQUIRED_MODULES:
        if not importlib.util.find_spec(module):
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])

def ffmpeg_exists():
    return shutil.which("ffmpeg") or os.path.isfile(os.path.join(FFMPEG_DIR, "bin", "ffmpeg.exe"))

def get_ffmpeg_path():
    return os.path.join(FFMPEG_DIR, "bin", "ffmpeg.exe") if platform.system() == "Windows" else "ffmpeg"

def offer_ffmpeg():
    root = tk.Tk()
    root.withdraw()
    if messagebox.askyesno("FFmpeg not found", "FFmpeg is required for audio-only download. Download now?"):
        download_ffmpeg()

def download_ffmpeg():
    tmp_zip = "ffmpeg_temp.zip"
    urllib.request.urlretrieve(FFMPEG_URL, tmp_zip)
    with zipfile.ZipFile(tmp_zip, 'r') as zip_ref:
        zip_ref.extractall(FFMPEG_DIR)
    os.remove(tmp_zip)

check_and_install()
from yt_dlp import YoutubeDL

# ================== CONFIG ==================
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

# ================== LANGUAGE ==================
LANGUAGES = {
    "en_us": {
        "lang.name": "English-US",
        "app.title": "Video Downloader",
        "label.link": "Video Link:",
        "label.output": "Output Folder:",
        "button.choose": "Choose Folder",
        "option.audio_only": "Audio Only",
        "label.language": "Language:",
        "button.download": "Download",
        "console.title": "Console",
        "advanced.enable": "Enable Advanced Mode",
        "advanced.settings": "Edit Advanced Options",
        "advanced.proxy": "Proxy (e.g. socks5://127.0.0.1:9050)",
        "advanced.cookies": "Cookies File Path",
        "advanced.user_agent": "User-Agent",
        "advanced.headers": "Additional Headers",
        "advanced.save": "Save Settings",
        "unsupported.site": "⚠️ This site may not be supported by yt_dlp",
        "info.checking": "Checking site support...",
        "info.ready": "Ready to download."
    },
    "id_id": {
        "lang.name": "Bahasa Indonesia",
        "app.title": "Pengunduh Video",
        "label.link": "Tautan Video:",
        "label.output": "Folder Output:",
        "button.choose": "Pilih Folder",
        "option.audio_only": "Hanya Audio",
        "label.language": "Bahasa:",
        "button.download": "Unduh",
        "console.title": "Konsol",
        "advanced.enable": "Aktifkan Mode Lanjutan",
        "advanced.settings": "Atur Opsi Lanjutan",
        "advanced.proxy": "Proxy (contoh: socks5://127.0.0.1:9050)",
        "advanced.cookies": "Path File Cookies",
        "advanced.user_agent": "User-Agent",
        "advanced.headers": "Header Tambahan",
        "advanced.save": "Simpan Pengaturan",
        "unsupported.site": "⚠️ Situs ini mungkin tidak didukung oleh yt_dlp",
        "info.checking": "Memeriksa dukungan situs...",
        "info.ready": "Siap untuk mengunduh."
    }
}

active_lang = LANGUAGES["en_us"]

def load_language(code):
    global active_lang
    active_lang = LANGUAGES.get(code, LANGUAGES["en_us"])

def get_text(key):
    return active_lang.get(key, key)

# ================== GUI ==================
def download_video(url, output, audio_only, config, log_func):
    ydl_opts = {
        "outtmpl": os.path.join(output, "%(title)s.%(ext)s"),
        "progress_hooks": [lambda d: log_func(d.get("status", "") + ": " + d.get("filename", ""))]
    }
    if config["advanced"]["enabled"]:
        if config["advanced"]["proxy"]:
            ydl_opts["proxy"] = config["advanced"]["proxy"]
        if config["advanced"]["cookies"]:
            ydl_opts["cookiefile"] = config["advanced"]["cookies"]
        if config["advanced"]["user_agent"]:
            ydl_opts["user_agent"] = config["advanced"]["user_agent"]
        if config["advanced"]["headers"]:
            ydl_opts["http_headers"] = dict(line.split(": ", 1) for line in config["advanced"]["headers"].splitlines() if ": " in line)

    if audio_only:
        if not ffmpeg_exists():
            offer_ffmpeg()
        ydl_opts.update({
            "format": "bestaudio",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "ffmpeg_location": get_ffmpeg_path()
        })
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        log_func("[Done] Download finished")
    except Exception as e:
        log_func(f"[Error] {str(e)}")

def launch_gui(config):
    load_language(config.get("language", "en_us"))
    root = tk.Tk()
    root.title(get_text("app.title"))
    root.geometry("600x480")
    root.resizable(False, False)

    url_var = tk.StringVar()
    output_var = tk.StringVar(value=config.get("output_path", ""))
    audio_only_var = tk.BooleanVar(value=config.get("audio_only", False))
    adv_mode_var = tk.BooleanVar(value=config["advanced"]["enabled"])
    log_box = None

    def browse_folder():
        folder = filedialog.askdirectory()
        if folder:
            output_var.set(folder)

    def run_download():
        config["output_path"] = output_var.get()
        config["audio_only"] = audio_only_var.get()
        config["advanced"]["enabled"] = adv_mode_var.get()
        save_config(config)
        threading.Thread(target=download_video, args=(url_var.get(), output_var.get(), audio_only_var.get(), config, log), daemon=True).start()

    def log(msg):
        log_box.insert(tk.END, msg + "\n")
        log_box.see(tk.END)

    frm = ttk.Frame(root, padding=10)
    frm.pack(fill="both", expand=True)

    ttk.Label(frm, text=get_text("label.link")).grid(row=0, column=0, sticky="w")
    ttk.Entry(frm, textvariable=url_var, width=60).grid(row=0, column=1, columnspan=2)

    ttk.Label(frm, text=get_text("label.output")).grid(row=1, column=0, sticky="w")
    ttk.Entry(frm, textvariable=output_var, width=45).grid(row=1, column=1)
    ttk.Button(frm, text=get_text("button.choose"), command=browse_folder).grid(row=1, column=2)

    ttk.Checkbutton(frm, text=get_text("option.audio_only"), variable=audio_only_var).grid(row=2, column=0, sticky="w")
    ttk.Checkbutton(frm, text=get_text("advanced.enable"), variable=adv_mode_var).grid(row=2, column=1, sticky="w")

    ttk.Button(frm, text=get_text("button.download"), command=run_download).grid(row=3, column=2, pady=5)

    ttk.Label(frm, text=get_text("console.title")).grid(row=4, column=0, columnspan=3, sticky="w")
    log_box = scrolledtext.ScrolledText(frm, height=12, width=70)
    log_box.grid(row=5, column=0, columnspan=3)

    ttk.Label(frm, text=get_text("label.language")).grid(row=6, column=0, sticky="w")
    lang_codes = list(LANGUAGES.keys())
    lang_names = [LANGUAGES[c]["lang.name"] for c in lang_codes]
    current_lang = config.get("language", "en_us")
    lang_var = tk.StringVar(value=LANGUAGES[current_lang]["lang.name"])

    def change_language(*args):
        selected = lang_var.get()
        idx = lang_names.index(selected)
        config["language"] = lang_codes[idx]
        save_config(config)
        messagebox.showinfo("Restart", "Please restart the app to apply language changes.")

    ttk.OptionMenu(frm, lang_var, lang_var.get(), *lang_names, command=change_language).grid(row=6, column=1)
    root.mainloop()

if __name__ == "__main__":
    config = load_config()
    launch_gui(config)
