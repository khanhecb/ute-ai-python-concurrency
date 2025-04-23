#!/usr/bin/python

from __future__ import print_function  # Đặt ở đầu file

from gevent import monkey
monkey.patch_all()  # Gọi monkey patch sớm nhất có thể

import gevent
import yt_dlp
import time

video_urls = [
    'https://www.youtube.com/watch?v=XqZsoesa55w',
    'https://www.youtube.com/watch?v=e_04ZrNroTo',
    'https://www.youtube.com/watch?v=YVVTZgwYwVo'
]

def download_video(url):
    ydl_opts = {
        'outtmpl': 'downloaded_videos/%(title)s.%(ext)s',  # Tên file duy nhất dựa trên tiêu đề
        'format': 'worst',  # Tải video với chất lượng thấp nhất
        'merge_output_format': 'mp4'  # Tự động chuyển thành MP4
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            print(f"🔄 Đang tải: {url}")
            ydl.download([url])
            print(f"✅ Tải xong: {url}\n")
        except Exception as e:
            print(f"❌ Lỗi khi tải {url}: {e}")


start = time.time()
# Tạo các công việc tải video
jobs = [gevent.spawn(download_video, url) for url in video_urls]

# Chờ tất cả công việc hoàn thành
gevent.wait(jobs)

print("Elapsed time:", time.time() - start, "seconds")
