import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import threading
import os
import re
from yt_dlp import YoutubeDL
from config import save_config, update_advanced_options
from lang import get_text, list_languages
from config import load_config
from lang import load_language

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
        ydl_opts.update({
            "format": "bestaudio",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]
        })
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        log_func("[Done] Download finished")
    except Exception as e:
        log_func(f"[Error] {str(e)}")

def is_supported_url(url):
    domain = re.findall(r"https?://(?:www\.)?([^/]+)", url)
    if domain:
        with os.popen("yt-dlp --list-extractors") as f:
            extractors = f.read().lower()
        return domain[0].lower() in extractors
    return False

def edit_advanced(config):
    win = tk.Toplevel()
    win.title(get_text("advanced.settings"))
    win.geometry("400x300")

    entries = {}
    fields = ["proxy", "cookies", "user_agent", "headers"]

    for i, field in enumerate(fields):
        tk.Label(win, text=get_text(f"advanced.{field}")).grid(row=i, column=0, sticky="w")
        entry = tk.Text(win, height=2 if field == "headers" else 1, width=40)
        entry.insert("1.0", config["advanced"].get(field, ""))
        entry.grid(row=i, column=1)
        entries[field] = entry

    def save():
        update_advanced_options({field: entries[field].get("1.0", "end").strip() for field in fields})
        messagebox.showinfo("Saved", get_text("advanced.save"))
        win.destroy()

    tk.Button(win, text=get_text("advanced.save"), command=save).grid(row=len(fields), columnspan=2)

def launch_gui(config):
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
        url = url_var.get().strip()
        if not url:
            log("[!] Empty URL")
            return
        log(get_text("info.checking"))
        if not is_supported_url(url):
            log(get_text("unsupported.site"))
        config["output_path"] = output_var.get()
        config["audio_only"] = audio_only_var.get()
        config["advanced"]["enabled"] = adv_mode_var.get()
        save_config(config)

        threading.Thread(
            target=download_video,
            args=(url, output_var.get(), audio_only_var.get(), config, log),
            daemon=True
        ).start()

    def log(message):
        log_box.insert(tk.END, message + "\n")
        log_box.see(tk.END)

    # GUI Layout
    frm = ttk.Frame(root, padding=10)
    frm.pack(fill="both", expand=True)

    ttk.Label(frm, text=get_text("label.link")).grid(row=0, column=0, sticky="w")
    ttk.Entry(frm, textvariable=url_var, width=60).grid(row=0, column=1, columnspan=2)

    ttk.Label(frm, text=get_text("label.output")).grid(row=1, column=0, sticky="w")
    ttk.Entry(frm, textvariable=output_var, width=45).grid(row=1, column=1)
    ttk.Button(frm, text=get_text("button.choose"), command=browse_folder).grid(row=1, column=2)

    ttk.Checkbutton(frm, text=get_text("option.audio_only"), variable=audio_only_var).grid(row=2, column=0, sticky="w")
    ttk.Checkbutton(frm, text=get_text("advanced.enable"), variable=adv_mode_var).grid(row=2, column=1, sticky="w")
    ttk.Button(frm, text=get_text("advanced.settings"), command=lambda: edit_advanced(config)).grid(row=2, column=2)

    ttk.Button(frm, text=get_text("button.download"), command=run_download).grid(row=3, column=2, pady=5)

    ttk.Label(frm, text=get_text("console.title")).grid(row=4, column=0, columnspan=3, sticky="w")
    log_box = scrolledtext.ScrolledText(frm, height=12, width=70)
    log_box.grid(row=5, column=0, columnspan=3)

    ttk.Label(frm, text=get_text("label.language")).grid(row=6, column=0, sticky="w")
    langs = list_languages()
    lang_codes = [code for code, _ in langs]
    lang_names = [name for _, name in langs]
    current_lang = config.get("language", "en_us")
    lang_var = tk.StringVar(value=lang_names[lang_codes.index(current_lang)] if current_lang in lang_codes else lang_names[0])

    def change_language(event=None):
        selected_name = lang_var.get()
        idx = lang_names.index(selected_name)
        lang_code = lang_codes[idx]
        config["language"] = lang_code
        save_config(config)
        load_language(lang_code)
        messagebox.showinfo("Restart Required", "Please restart the application to apply language change.")

    ttk.OptionMenu(frm, lang_var, *lang_names, command=change_language).grid(row=6, column=1)

    root.mainloop()
