from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    add_review_view,
    similar_books_view,
    recommend_for_user_view,
    toggle_favorite,
)

app_name = "book"

urlpatterns = [
    path("", BookListView.as_view(), name="book_list"),
    path("<int:pk>/", BookDetailView.as_view(), name="book_detail"),
    path("recommend/", recommend_for_user_view, name="recommend_user"),
    path("<int:pk>/similar/", similar_books_view, name="similar_books"),
    path("review/add/<int:book_id>/", add_review_view, name="add_review"),
    path("favorite/<int:book_id>/", toggle_favorite, name="toggle_favorite"),

]
