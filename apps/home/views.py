from django.views.generic import TemplateView
from apps.book.models import Book, Category, Review

class HomeView(TemplateView):
    template_name = "home/home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Sách mới nhất
        context['new_books'] = Book.objects.all().order_by('-published_date')[:12]
        
        # Sách bán chạy (giả lập)
        context['bestsellers'] = Book.objects.all().order_by('?')[:12]
        
        # Danh mục
        context['categories'] = Category.objects.all()[:6]
        
        # AI Recommendations
        if self.request.user.is_authenticated:
            user_reviews = Review.objects.filter(user=self.request.user)
            if user_reviews.exists():
                reviewed_categories = set([review.book.category for review in user_reviews])
                ai_books = Book.objects.filter(category__in=reviewed_categories).exclude(
                    id__in=[review.book.id for review in user_reviews]
                ).order_by('?')[:8]
            else:
                ai_books = Book.objects.all().order_by('?')[:8]
            context['ai_recommendations'] = ai_books
        
        return context
