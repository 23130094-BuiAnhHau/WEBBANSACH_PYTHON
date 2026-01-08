from django.db.models import Avg
from django.contrib.auth import get_user_model
from django.apps import apps

from apps.order.models import OrderItem

User = get_user_model()

Book = apps.get_model("book", "Book")
Review = apps.get_model("book", "Review")
BookViewHistory = apps.get_model("book", "BookViewHistory")
FavoriteBook = apps.get_model("book", "FavoriteBook")
RecommendationCache = apps.get_model("book", "RecommendationCache")


class BookRecommender:
    @staticmethod
    def get_user_history_ids(user):
        """
        Trả về tập book_id mà user đã từng tương tác
        (mua, xem, yêu thích, đánh giá)
        """
        purchased = set(
            OrderItem.objects.filter(order__user=user)
            .values_list("book_id", flat=True)
        )

        viewed = set(
            BookViewHistory.objects.filter(user=user)
            .values_list("book_id", flat=True)
        )

        favorites = set(
            FavoriteBook.objects.filter(user=user)
            .values_list("book_id", flat=True)
        )

        reviewed = set(
            Review.objects.filter(user=user)
            .values_list("book_id", flat=True)
        )

        return purchased | viewed | favorites | reviewed

    @staticmethod
    def similar_books(book, limit=50):
        """
        Gợi ý sách tương tự:
        1. Cùng tác giả
        2. Cùng thể loại
        3. Rating cao
        """
        if not isinstance(book, Book):
            return Book.objects.none()

        qs = Book.objects.exclude(id=book.id)
        result = []

        # 1. Cùng tác giả
        same_author = list(qs.filter(author=book.author)[:limit])
        result.extend(same_author)

        if len(result) >= limit:
            return result[:limit]

        # 2. Cùng thể loại
        if book.category:
            same_category = list(
                qs.filter(category=book.category)
                .exclude(id__in=[b.id for b in result])[: limit - len(result)]
            )
            result.extend(same_category)

        if len(result) >= limit:
            return result[:limit]

        # 3. Bù bằng rating cao
        more = list(
            qs.exclude(id__in=[b.id for b in result])
            .annotate(avg_rating=Avg("reviews__rating"))
            .order_by("-avg_rating")[: limit - len(result)]
        )
        result.extend(more)

        return result[:limit]

    @staticmethod
    def compute_user_scores(user):
        """
        Tính điểm gợi ý cho toàn bộ sách dựa trên:
        - Sách đã mua
        - Sách yêu thích
        - Thể loại đã quan tâm
        - Lượt xem
        - Đánh giá
        - Bán chạy
        """
        # Xóa cache cũ
        RecommendationCache.objects.filter(user=user).delete()

        #láy dữ liệu user
        purchased_ids = set(
            OrderItem.objects.filter(order__user=user)
            .values_list("book_id", flat=True)
        )

        favorite_ids = set(
            FavoriteBook.objects.filter(user=user)
            .values_list("book_id", flat=True)
        )

        viewed_ids = set(
            BookViewHistory.objects.filter(user=user)
            .values_list("book_id", flat=True)
        )

        # thể loại user quan tâm 
        preferred_categories = set(
            Book.objects.filter(id__in=purchased_ids | favorite_ids)
            .values_list("category_id", flat=True)
        )

        caches = []

        for book in Book.objects.all():
            score = 0.0

            # sách đã thích
            if book.id in favorite_ids:
                score += 6.0

            #  sách đã mua
            if book.id in purchased_ids:
                score += 4.0

            #  cùng thể oại
            if book.category_id in preferred_categories:
                score += 5.0

            #  sách đã xem
            if book.id in viewed_ids:
                score += 2.0

            # điểm đanh giá trung bình
            avg_rating = Review.objects.filter(book=book).aggregate(
                avg=Avg("rating")
            )["avg"] or 0.0
            score += avg_rating * 0.5

            #  lượt xem
            view_count = BookViewHistory.objects.filter(book=book).count()
            score += view_count * 0.2

            #  bán chạy
            sold_count = OrderItem.objects.filter(book=book).count()
            score += sold_count * 0.1

            caches.append(
                RecommendationCache(user=user, book=book, score=score)
            )

        RecommendationCache.objects.bulk_create(caches)
        return RecommendationCache.objects.filter(user=user).order_by("-score")

    @staticmethod
    def recommend(user, limit=50):
        """
        Trả về danh sách Book gợi ý cho user
        """
        # Guest -> sách rating cao
        if user is None or not user.is_authenticated:
            return list(
                Book.objects.annotate(avg_rating=Avg("reviews__rating"))
                .order_by("-avg_rating")[:limit]
            )

        # Có cache -> dùng cache
        cache_qs = RecommendationCache.objects.filter(user=user).order_by("-score")
        if cache_qs.exists():
            ids = list(cache_qs.values_list("book_id", flat=True)[:limit])
            books = list(Book.objects.filter(id__in=ids))

            # giữ đúng thứ tự score
            id_order = {id_: idx for idx, id_ in enumerate(ids)}
            books.sort(key=lambda b: id_order.get(b.id, 999))

            return books

        # Chưa có cache -> tính rồi trả về
        cache_qs = BookRecommender.compute_user_scores(user)
        ids = list(cache_qs.values_list("book_id", flat=True)[:limit])
        books = list(Book.objects.filter(id__in=ids))

        id_order = {id_: idx for idx, id_ in enumerate(ids)}
        books.sort(key=lambda b: id_order.get(b.id, 999))

        return books
