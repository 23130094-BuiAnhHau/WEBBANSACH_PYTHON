# apps/book/middleware.py
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import resolve_url

from .models import BookViewHistory, Book

class BookViewTrackingMiddleware(MiddlewareMixin):
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            if request.user.is_authenticated and 'pk' in view_kwargs:
                pk = view_kwargs.get('pk')
                book = Book.objects.filter(pk=pk).first()
                if book:
                    BookViewHistory.objects.create(user=request.user, book=book)
        except Exception:
            pass
        return None
