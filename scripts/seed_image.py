import os
import sys
import django
import requests
from django.core.files.base import ContentFile
from urllib.parse import quote

# CẤU HÌNH DJANGO
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BookStore.settings")
django.setup()

from apps.book.models import Book

GOOGLE_BOOK_API = "https://www.googleapis.com/books/v1/volumes"
OPEN_LIBRARY_API = "https://openlibrary.org/search.json"

def get_cover_google(title, author):
    """Tìm ảnh bìa từ Google Books"""
    try:
        query = f"{title} {author}"
        r = requests.get(GOOGLE_BOOK_API, params={"q": query, "maxResults": 5}, timeout=10)
        if r.status_code != 200:
            return None
        data = r.json()
        if "items" not in data:
            return None
        # Duyệt qua nhiều item, chọn cái có ảnh lớn nhất
        best_url = None
        max_size = 0
        for item in data["items"]:
            info = item.get("volumeInfo", {})
            imgs = info.get("imageLinks", {})
            for key in ["extraLarge", "large", "medium", "thumbnail", "smallThumbnail"]:
                if key in imgs:
                    url = imgs[key]
                    # ưu tiên URL dài hơn = ảnh chất lượng hơn
                    if len(url) > max_size:
                        max_size = len(url)
                        best_url = url
        return best_url
    except:
        return None

def get_cover_openlibrary(title, author):
    """Fallback Open Library"""
    try:
        query = quote(f"{title} {author}")
        r = requests.get(f"{OPEN_LIBRARY_API}?title={query}&limit=1", timeout=10)
        if r.status_code != 200:
            return None
        data = r.json()
        if "docs" not in data or len(data["docs"]) == 0:
            return None
        doc = data["docs"][0]
        cover_id = doc.get("cover_i")
        if cover_id:
            return f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
    except:
        return None

def seed_book_covers(force=False):
    books = Book.objects.all()
    for book in books:
        print(f"Đang xử lý: {book.title} - {book.author}")
        if book.cover_image and not force:
            print(" → Đã có ảnh, bỏ qua")
            continue

        url = get_cover_google(book.title, book.author)
        if not url:
            url = get_cover_openlibrary(book.title, book.author)

        if not url:
            print(" → Không tìm thấy ảnh chuẩn, bỏ qua")
            continue

        try:
            img_data = requests.get(url, timeout=10).content
            filename = f"{book.title.replace(' ', '_')}_{book.id}.jpg"
            book.cover_image.save(filename, ContentFile(img_data), save=True)
            print(" → Đã tải ảnh thành công")
        except Exception as e:
            print(f" → Lỗi tải ảnh: {e}")

if __name__ == "__main__":
    print("Bắt đầu seed ảnh bìa sách...")
    seed_book_covers(force=False)
    print("Hoàn tất!")
