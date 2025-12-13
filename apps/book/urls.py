from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    similar_books_view,
    recommend_for_user_view,
)

app_name = "book"

urlpatterns = [
    path("", BookListView.as_view(), name="book_list"),
    path("<int:pk>/", BookDetailView.as_view(), name="book_detail"),
    path("recommend/", recommend_for_user_view, name="recommend_user"),
    path("<int:pk>/similar/", similar_books_view, name="similar_books"),
]
