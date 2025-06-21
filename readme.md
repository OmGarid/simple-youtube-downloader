# 🎬 Simple YouTube Downloader

A simple, elegant YouTube video & playlist downloader with GUI built using `tkinter` and `yt_dlp`.  
Supports multilingual interface, folder selection, audio-only mode, and automatic dependency installation.

## 🚀 Features
- ✅ Download single videos or full playlists
- 🌐 Multilingual support (`en_us`, `id_id`)
- 🎵 Audio-only mode (auto-install FFmpeg if needed)
- 🗂 Choose custom output folder
- 🧵 Runs download in separate thread (UI won't freeze)
- 🌗 Light & Dark theme (system-based)

## 🧰 Dependencies
Auto-installed on first run:
- `yt_dlp`
- `tkinter`
- `requests` (optional for FFmpeg download)
- `rich` (optional console, CLI)

## 📦 How to Use

### 🔧 Run GUI App

```bash
python main.py
```

### 🌍 Change Language via Command Line

```bash
python main.py -l en_us
python main.py -l id_id
```

### ⚙️ Open Config Editor (WIP)

```bash
python main.py -s
```

### 🔗 Or Start Download via CLI (Optional)

```bash
python main.py https://youtu.be/example123
```

## 📁 Output Folder
<p>Downloads will be saved to the folder you selected.</p>

<br>
<br>

### Made with ❤️ using Python
