from concurrent.futures import ThreadPoolExecutor
import yt_dlp
import os
import time

# Danh sách URL video cần tải
video_urls = [
    'https://www.youtube.com/watch?v=XqZsoesa55w',
    'https://www.youtube.com/watch?v=e_04ZrNroTo',
    'https://www.youtube.com/watch?v=YVVTZgwYwVo'
]

# Tạo thư mục lưu video nếu chưa tồn tại
if not os.path.exists('downloaded_videos'):
    os.makedirs('downloaded_videos')

start = time.time()

# Hàm tải video
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

# Sử dụng ThreadPoolExecutor để tải video song song
with ThreadPoolExecutor(max_workers=3) as executor:  # Số luồng tối đa
    executor.map(download_video, video_urls)
    
print("Elapsed time:", time.time() - start, "seconds")
