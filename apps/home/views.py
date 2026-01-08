from django.views.generic import TemplateView
from django.db.models import Count, Prefetch
from apps.book.models import Book, Category, BookImage
from apps.book.ai.recommender import BookRecommender
from apps.home.models import Banner


class HomeView(TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Banner active đầu tiên
        context["banner"] = Banner.objects.filter(is_active=True).first()

        # Query ảnh hợp lệ
        image_qs = BookImage.objects.exclude(image="").exclude(image__isnull=True)

        # SÁCH MỚI NHẤT
        context["new_books"] = (
            Book.objects
            .order_by("-created_at")
            .prefetch_related(
                Prefetch("images", queryset=image_qs)
            )[:12]
        )

        # SÁCH BÁN CHẠY
        context["bestsellers"] = (
            Book.objects
            .annotate(sold_count=Count("orderitem"))
            .order_by("-sold_count")
            .prefetch_related(
                Prefetch("images", queryset=image_qs)
            )[:12]
        )

        # DANH MỤC
        context["categories"] = Category.objects.all()

        # AI RECOMMEND
        user = self.request.user
        if user.is_authenticated:
            ai_books = BookRecommender.recommend(user, limit=8)

            context["ai_recommendations"] = (
                Book.objects
                .filter(id__in=[b.id for b in ai_books])
                .prefetch_related(
                    Prefetch("images", queryset=image_qs)
                )
            )

        else:
            context["ai_recommendations"] = []

        return context
