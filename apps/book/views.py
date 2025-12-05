from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from apps.book.models import Book, Category
from django.db.models import Q

# --- Danh sách sách ---
class BookListView(ListView):
    model = Book
    template_name = "templates/book_list.html"
    context_object_name = "books"
    paginate_by = 12

    def get_queryset(self):
        qs = Book.objects.all()
        # --- Lọc theo tìm kiếm ---
        search = self.request.GET.get("search")
        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(author__icontains=search))
        # --- Lọc theo danh mục ---
        category_id = self.request.GET.get("category")
        if category_id:
            qs = qs.filter(category__id=category_id)
        # --- Sắp xếp ---
        sort = self.request.GET.get("sort")
        if sort == "price_asc":
            qs = qs.order_by("price")
        elif sort == "price_desc":
            qs = qs.order_by("-price")
        elif sort == "title":
            qs = qs.order_by("title")
        elif sort == "author":
            qs = qs.order_by("author")
        return qs

# --- Chi tiết sách ---
class BookDetailView(DetailView):
    model = Book
    template_name = "templates/book_detail.html"
    context_object_name = "book"
