from django.views.generic import TemplateView
from django.db.models import Count
from apps.book.models import Book, Category
from apps.book.ai.recommender import BookRecommender


class HomeView(TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #  SÁCH MỚI NHẤT (theo created_at)
        context["new_books"] = Book.objects.order_by("-created_at")[:12]

        #  SÁCH BÁN CHẠY (dựa OrderItem)
        context["bestsellers"] = (
            Book.objects
            .annotate(sold_count=Count("orderitem"))
            .order_by("-sold_count")[:12]
        )

        #  DANH MỤC
        context["categories"] = Category.objects.all()

        #  AI RECOMMEND
        user = self.request.user
        if user.is_authenticated:
            context["ai_recommendations"] = BookRecommender.recommend(user, limit=8)
        else:
            context["ai_recommendations"] = []

        return context
