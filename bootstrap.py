import importlib.util
import subprocess
import sys
import os
import platform
import urllib.request
import zipfile
import shutil

REQUIRED_MODULES = ["yt_dlp", "tkinter", "rich"]
FFMPEG_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
FFMPEG_DIR = "ffmpeg"

def check_and_install():
    for module in REQUIRED_MODULES:
        if not importlib.util.find_spec(module):
            print(f"[!] Installing: {module}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])

def ffmpeg_exists():
    if shutil.which("ffmpeg"):
        return True
    return os.path.isfile(os.path.join(FFMPEG_DIR, "bin", "ffmpeg.exe"))

def get_ffmpeg_path():
    if platform.system() == "Windows":
        return os.path.join(FFMPEG_DIR, "bin", "ffmpeg.exe")
    return "ffmpeg"

def offer_ffmpeg():
    from tkinter import messagebox
    from tkinter import Tk
    root = Tk()
    root.withdraw()
    result = messagebox.askyesno("FFmpeg not found", "FFmpeg diperlukan untuk audio only.\nDownload sekarang?")
    if result:
        download_ffmpeg()

def download_ffmpeg():
    tmp_zip = "ffmpeg_temp.zip"
    urllib.request.urlretrieve(FFMPEG_URL, tmp_zip)
    with zipfile.ZipFile(tmp_zip, 'r') as zip_ref:
        zip_ref.extractall("ffmpeg")
    os.remove(tmp_zip)

def bootstrap():
    check_and_install()
