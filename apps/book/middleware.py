# apps/book/middleware.py
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import resolve_url

from .models import BookViewHistory, Book

class BookViewTrackingMiddleware(MiddlewareMixin):
    """
    Middleware rất nhẹ: nếu request truy cập view có kwarg 'pk' và object là Book,
    sẽ lưu record BookViewHistory cho user đã đăng nhập.
    """
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if request.user.is_authenticated and 'pk' in view_kwargs:
                pk = view_kwargs.get('pk')
                # không raise nếu book không tồn tại
                book = Book.objects.filter(pk=pk).first()
                if book:
                    BookViewHistory.objects.create(user=request.user, book=book)
        except Exception:
            # không muốn middleware làm crash toàn bộ trang
            pass
        return None
