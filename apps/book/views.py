# apps/book/views.py

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.db.models import Count

from apps.book.models import Book, Category, Review
from apps.book.ai.recommender import BookRecommender
from apps.order.models import OrderItem
from django.contrib.auth.decorators import login_required
from django.db.models import Avg


# List view dùng ListView
class BookListView(ListView):
    model = Book
    template_name = "book/book_list.html"
    context_object_name = "books"
    paginate_by = 12

    def get_queryset(self):
        qs = Book.objects.all()

        # LỌC THEO DANH MỤC
        category_id = self.request.GET.get("category")
        if category_id:
            qs = qs.filter(category_id=category_id)

        # SEARCH
        search = self.request.GET.get("search")
        if search:
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(author__name__icontains=search)
            )

        # SORT
        sort = self.request.GET.get("sort")
        if sort == "price_asc":
            qs = qs.order_by("sale_price", "price")
        elif sort == "price_desc":
            qs = qs.order_by("-sale_price", "-price")
        elif sort == "title":
            qs = qs.order_by("title")
        elif sort == "author":
            qs = qs.order_by("author__name")
        elif sort == "new":
            qs = qs.order_by("-created_at")
        elif sort == "bestseller":
            qs = qs.annotate(
                sold=Count("orderitem")
            ).order_by("-sold")

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = Category.objects.all()

        category_id = self.request.GET.get("category")
        if category_id:
            ctx["current_category"] = Category.objects.filter(id=category_id).first()

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


def user_has_bought_book(user, book):
    return OrderItem.objects.filter(
        order__user=user,
        order__status="Completed",
        book=book
    ).exists()

@login_required
def add_review_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    # Kiểm tra đã mua sách chưa
    has_bought = OrderItem.objects.filter(
        order__user=request.user,
        order__status="Completed",
        book=book
    ).exists()

    if not has_bought:
        messages.error(request, "Bạn chỉ có thể đánh giá sách sau khi đã mua.")
        return redirect("book:book_detail", pk=book.id)

    #  Kiểm tra đã review chưa
    if Review.objects.filter(book=book, user=request.user).exists():
        messages.warning(request, "Bạn đã đánh giá sách này rồi.")
        return redirect("book:book_detail", pk=book.id)

    #  Xử lý POST
    if request.method == "POST":
        rating = int(request.POST.get("rating", 5))
        comment = request.POST.get("comment", "")

        Review.objects.create(
            book=book,
            user=request.user,
            rating=rating,
            comment=comment
        )

        #  Cập nhật average_rating cho Book 
        avg_rating = book.reviews.aggregate(avg=Avg("rating"))["avg"] or 0
        book.average_rating = round(avg_rating, 1)
        book.save(update_fields=["average_rating"])

        messages.success(request, "Đánh giá của bạn đã được ghi nhận.")
        return redirect("book:book_detail", pk=book.id)

    return render(request, "book/add_review.html", {"book": book})

