import yt_dlp
import os
import time
from concurrent.futures import ThreadPoolExecutor

video_urls = [
    'https://www.youtube.com/watch?v=XqZsoesa55w',
    'https://www.youtube.com/watch?v=e_04ZrNroTo',
    'https://www.youtube.com/watch?v=YVVTZgwYwVo'
]

if not os.path.exists('downloaded_videos'):
    os.makedirs('downloaded_videos')

start = time.time()

def download_video(url):
    ydl_opts = {
        'outtmpl': 'downloaded_videos/%(title)s.%(ext)s',
        'format': 'worst',
        'merge_output_format': 'mp4'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            print(f"🔄 Đang tải: {url}")
            ydl.download([url])
            print(f"✅ Tải xong: {url}\n")
        except Exception as e:
            print(f"❌ Lỗi khi tải {url}: {e}")

for url in video_urls:
    download_video(url)
    
print("⏱️ Elapsed time:", time.time() - start, "seconds")

