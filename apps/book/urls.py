from django.urls import path
from apps.book.views import BookListView, BookDetailView

urlpatterns = [
    path("", BookListView.as_view(), name="book_list"),             # Danh sách sách
    path("<int:pk>/", BookDetailView.as_view(), name="book_detail"), # Chi tiết sách
]
