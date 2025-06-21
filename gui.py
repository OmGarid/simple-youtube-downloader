# gui.py
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from threading import Thread
from downloader import download_video
from config import save_config
from lang import get_text, set_active_language, list_languages
import os

def launch_gui(config):
    set_active_language(config["language"])

    root = tk.Tk()
    root.title(get_text("app.title"))
    root.geometry("600x480")
    root.resizable(False, False)

    theme = config.get("theme", "dark")
    if theme == "dark":
        bg, fg, accent = "#111", "#fff", "#00ff88"
    elif theme == "light":
        bg, fg, accent = "#f2f2f2", "#111", "#008844"
    else:  # follow system (default to dark for now)
        bg, fg, accent = "#111", "#fff", "#00ff88"

    root.configure(bg=bg)

    link_var = tk.StringVar()
    audio_var = tk.BooleanVar(value=False)
    lang_keys, lang_names = list_languages()
    if config["language"] not in lang_keys:
        config["language"] = "en_us"  # fallback
        save_config(config)

    lang_var = tk.StringVar(value=lang_names[lang_keys.index(config["language"])])


    # Link Input
    tk.Label(root, text=get_text("label.link"), bg=bg, fg=fg).pack(anchor="w", padx=10, pady=(10, 0))
    tk.Entry(root, textvariable=link_var, width=80).pack(padx=10)

    # Output Folder
    tk.Label(root, text=get_text("label.output"), bg=bg, fg=fg).pack(anchor="w", padx=10, pady=(10, 0))
    output_label = tk.Label(root, text=config["output_dir"], bg=bg, fg=accent)
    output_label.pack(anchor="w", padx=10)

    def choose_folder():
        folder = filedialog.askdirectory()
        if folder:
            config["output_dir"] = folder
            output_label.config(text=folder)
            save_config(config)

    tk.Button(root, text=get_text("button.choose"), command=choose_folder).pack(padx=10, pady=(0, 10))

    # Audio Only Checkbox
    tk.Checkbutton(root, text=get_text("option.audio_only"), variable=audio_var, bg=bg, fg=fg, selectcolor=bg).pack(anchor="w", padx=10)

    # Language Dropdown
    tk.Label(root, text=get_text("label.language"), bg=bg, fg=fg).pack(anchor="w", padx=10)
    lang_menu = ttk.Combobox(root, textvariable=lang_var, values=lang_names, state="readonly")
    lang_menu.pack(padx=10)

    # Console Output
    log_frame = tk.LabelFrame(root, text=get_text("console.title"), bg=bg, fg=fg)
    log_frame.pack(fill="both", expand=True, padx=10, pady=10)
    log_text = tk.Text(log_frame, height=8, bg="#000", fg="#0f0", insertbackground="#0f0")
    log_text.pack(fill="both", expand=True)

    def log(msg):
        log_text.insert(tk.END, msg + "\n")
        log_text.see(tk.END)

    # Download Button
    def start_download():
        link = link_var.get().strip()
        if not link:
            messagebox.showerror("Error", get_text("error.empty_link"))
            return
        Thread(target=download_video, args=(link, config["output_dir"], audio_var.get(), log)).start()

    tk.Button(root, text=get_text("button.download"), bg=accent, fg="black", command=start_download).pack(padx=10, pady=10)

    # Language Change Action
    def change_lang(evt):
        index = lang_names.index(lang_var.get())
        new_code = lang_keys[index]
        config["language"] = new_code
        save_config(config)
        set_active_language(new_code)
        root.destroy()
        launch_gui(config)

    lang_menu.bind("<<ComboboxSelected>>", change_lang)

    root.mainloop()
