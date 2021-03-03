#!/usr/bin/python3
import os
import sys

import youtube_dl

work_dir = os.path.abspath(os.path.dirname(__file__))
save_folder = "downloads"


def y2b_download(url):
    filename = '%(title)s.%(ext)s'
    ydl_opts = {
        'format': 'best[filesize<200M][ext=mp4]',
        'outtmpl': os.path.join(work_dir, save_folder, filename),
        'quiet': True,
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return os.path.split(filename)[-1]
    except BaseException as e:
        return e


def main():
    url = sys.argv[1]
    results = y2b_download(url)
    print(results)


if __name__ == "__main__":
    main()
