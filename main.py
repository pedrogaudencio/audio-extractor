from __future__ import unicode_literals
import os
from pathlib import Path
import shutil
import youtube_dl

HOME_FOLDER = os.path.expanduser('~')
DOWNLOADS_FOLDER = 'Downloads'
FILES_DOWLOAD_FOLDER = 'youtube_downloads'
DESTINATION_FOLDER = f"{HOME_FOLDER}/{DOWNLOADS_FOLDER}/{FILES_DOWLOAD_FOLDER}"
SOURCE_FILENAME = './audios.txt'
DOWNLOADED_FILES = []


class Logger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def read_file():
    with open(SOURCE_FILENAME) as f:
        return f.read().splitlines()


def downloading_hook(audio):
    if (audio['status'] == 'downloading' and
            audio.get('_percent_str') == '  0.0%'):

        print(f"Downloading {audio['filename']}... "
              f"ETA: {int(audio.get('eta')/60)}min")


def finished_hook(audio):
    if audio['status'] == 'finished':
        DOWNLOADED_FILES.append(audio.get('filename'))


def move_files():
    if not os.path.exists(DESTINATION_FOLDER):
        os.makedirs(DESTINATION_FOLDER)
    for file in DOWNLOADED_FILES:
        mp3_filename = f"./{os.path.splitext(file)[0]}.mp3"
        shutil.move(mp3_filename, DESTINATION_FOLDER)


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': Logger(),
    'progress_hooks': [downloading_hook, finished_hook],
}


with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    loaded_audios = read_file()
    ydl.download(loaded_audios)
    move_files()
