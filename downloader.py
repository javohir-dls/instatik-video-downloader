import os
import uuid
import yt_dlp

# Videolar vaqtincha saqlanadigan papka
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_video(url: str):
    # Har bir video uchun noyob nom yaratish
    file_id = str(uuid.uuid4())[:8]
    output = f"{DOWNLOAD_DIR}/{file_id}.%(ext)s"

    # Eng muhim sozlamalar
    ydl_opts = {
        "outtmpl": output,
        "format": "best[ext=mp4]/best",
        "merge_output_format": "mp4",
        "noplaylist": True,
        "quiet": False,
        "no_warnings": True,
        "socket_timeout": 60,
        "retries": 5,
        
        # Instagram va boshqalar uchun eng muhim qismlar:
        # Agar papkada cookies.txt bo'lsa, uni ishlatadi (Instagram uchun shart)
        "cookiefile": "cookies.txt" if os.path.exists("cookies.txt") else None,
        
        # Brauzer ekanligini bildirish uchun
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        
        # Yuklash tezligi va sifatini optimallashtirish
        "http_headers": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Ma'lumotlarni yuklash va fayl nomini olish
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

            # Fayl nomini .mp4 qilib saqlash
            if not filename.endswith(".mp4"):
                filename = filename.rsplit(".", 1)[0] + ".mp4"
                
            return filename
            
    except Exception as e:
        # Xatolik yuz bersa, uni konsolga chiqarish
        print(f"Yuklashda xatolik: {e}")
        return None
