import os
from yt_dlp import YoutubeDL
from threading import Thread
from bootstrap import ffmpeg_exists, offer_ffmpeg, get_ffmpeg_path

def download_video(url, config, logger, on_done):
    def run():
        output_dir = config.get("output_dir", os.getcwd())
        audio_only = config.get("audio_only", False)

        if audio_only and not ffmpeg_exists():
            offer_ffmpeg()

        ydl_opts = {
            'format': 'bestaudio/best' if audio_only else 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp3' if audio_only else 'mp4',
            'quiet': True,
            'ffmpeg_location': get_ffmpeg_path() if audio_only else None,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }] if audio_only else [],
            'progress_hooks': [lambda d: logger(d)]
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            on_done("✅ Selesai mengunduh.")
        except Exception as e:
            on_done(f"❌ Error: {e}")

    Thread(target=run).start()
