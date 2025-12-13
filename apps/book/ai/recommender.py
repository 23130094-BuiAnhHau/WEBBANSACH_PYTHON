# apps/book/ai/recommender.py
from apps.book.models import Book, Review, BookViewHistory, FavoriteBook, RecommendationCache
from apps.order.models import OrderItem
from django.db.models import Avg, Count
from django.contrib.auth import get_user_model

User = get_user_model()

class BookRecommender:
    @staticmethod
    def get_user_history_ids(user):
        """Trả về set các book.id user đã tương tác (mua/view/fav/review)."""
        purchased = set(OrderItem.objects.filter(order__user=user).values_list("book_id", flat=True))
        viewed = set(BookViewHistory.objects.filter(user=user).values_list("book_id", flat=True))
        favs = set(FavoriteBook.objects.filter(user=user).values_list("book_id", flat=True))
        reviews = set(Review.objects.filter(user=user).values_list("book_id", flat=True))
        return purchased | viewed | favs | reviews

    @staticmethod
    def similar_books(book, limit=6):
        """Gợi ý đơn giản: same author -> same category → top rating."""
        if not isinstance(book, Book):
            return Book.objects.none()

        qs = Book.objects.exclude(id=book.id)
        # 1) same author first
        same_author = list(qs.filter(author=book.author)[:limit])
        if len(same_author) >= limit:
            return same_author[:limit]
        result = same_author

        # 2) same category next
        if book.category:
            same_cat = list(qs.filter(category=book.category).exclude(id__in=[b.id for b in result])[:limit - len(result)])
            result.extend(same_cat)
        if len(result) >= limit:
            return result[:limit]

        # 3) fill by avg rating
        more = list(qs.exclude(id__in=[b.id for b in result])
                    .annotate(avg_rating=Avg("reviews__rating"))
                    .order_by("-avg_rating")[:limit - len(result)])
        result.extend(more)
        return result[:limit]

    @staticmethod
    def compute_user_scores(user):
        """Tính score cơ bản cho tất cả sách và lưu vào RecommendationCache."""
        # xóa cache cũ
        RecommendationCache.objects.filter(user=user).delete()

        user_history_ids = BookRecommender.get_user_history_ids(user)
        all_books = Book.objects.all()

        caches = []
        for b in all_books:
            score = 0.0
            # nếu user đã có tương tác -> +3
            if b.id in user_history_ids:
                score += 3.0

            # điểm trung bình review
            avg = Review.objects.filter(book=b).aggregate(avg=Avg("rating"))["avg"] or 0.0
            score += float(avg) * 0.5

            # view count
            views = BookViewHistory.objects.filter(book=b).count()
            score += views * 0.2

            # bán chạy (nếu OrderItem tồn tại)
            sold_count = OrderItem.objects.filter(book=b).aggregate(total=Count("id"))["total"] or 0
            score += float(sold_count) * 0.1

            caches.append(RecommendationCache(user=user, book=b, score=score))
        RecommendationCache.objects.bulk_create(caches)
        return RecommendationCache.objects.filter(user=user).order_by("-score")

    @staticmethod
    def recommend(user, limit=6):
        """Trả về list Book instances cho user."""
        if user is None or not user.is_authenticated:
            # guest: trả top rating
            return list(Book.objects.annotate(avg_rating=Avg("reviews__rating")).order_by("-avg_rating")[:limit])

        cache_qs = RecommendationCache.objects.filter(user=user).order_by("-score")
        if cache_qs.exists():
            # lấy book instances theo order score
            ids = list(cache_qs.values_list("book_id", flat=True)[:limit])
            books = list(Book.objects.filter(id__in=ids))
            # preserve order by ids
            id_pos = {id_: i for i, id_ in enumerate(ids)}
            books.sort(key=lambda b: id_pos.get(b.id, 999))
            return books

        # nếu không có cache -> compute then return
        cache_qs = BookRecommender.compute_user_scores(user)
        ids = list(cache_qs.values_list("book_id", flat=True)[:limit])
        books = list(Book.objects.filter(id__in=ids))
        id_pos = {id_: i for i, id_ in enumerate(ids)}
        books.sort(key=lambda b: id_pos.get(b.id, 999))
        return books
