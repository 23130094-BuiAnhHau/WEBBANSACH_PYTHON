# apps/book/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.db.models import Q

from apps.book.models import Book, Category
from apps.book.ai.recommender import BookRecommender

# List view dùng ListView
class BookListView(ListView):
    model = Book
    template_name = "book/book_list.html"
    context_object_name = "books"
    paginate_by = 12

    def get_queryset(self):
        qs = Book.objects.all()
        search = self.request.GET.get("search")
        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(author__name__icontains=search))
        category_id = self.request.GET.get("category")
        if category_id:
            qs = qs.filter(category__id=category_id)
        sort = self.request.GET.get("sort")
        if sort == "price_asc":
            qs = qs.order_by("price")
        elif sort == "price_desc":
            qs = qs.order_by("-price")
        elif sort == "title":
            qs = qs.order_by("title")
        elif sort == "author":
            qs = qs.order_by("author__name")
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = Category.objects.prefetch_related("books")
        ctx["search"] = self.request.GET.get("search", "")
        return ctx


# Detail view
class BookDetailView(DetailView):
    model = Book
    template_name = "book/book_detail.html"
    context_object_name = "book"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        book = self.object
        # Gợi ý tương tự bằng recommender
        ctx["similar_books"] = BookRecommender.similar_books(book, limit=6)
        return ctx

# Function view: similar (direct)
def similar_books_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    suggestions = BookRecommender.similar_books(book, limit=12)
    return render(request, "book/similar_books.html", {"book": book, "suggestions": suggestions})

# Gợi ý cho user
def recommend_for_user_view(request):
    if not request.user.is_authenticated:
        return render(request, "book/recommend_user.html", {"suggestions": [], "message": "Bạn cần đăng nhập để xem gợi ý."})
    suggestions = BookRecommender.recommend(request.user, limit=6)
    return render(request, "book/recommend_user.html", {"suggestions": suggestions})
