from django.contrib import admin
from django.db.models import Avg

from apps.book.models import (
    Category,
    Author,
    Book,
    BookImage,
    Review,
    ProductDiscount,
    BookViewHistory,
    FavoriteBook,
    RecommendationCache,
)


# cập nhật rating


def update_book_average_rating(book):
    avg = book.reviews.aggregate(avg=Avg("rating"))["avg"]
    book.average_rating = round(avg or 0, 1)
    book.save(update_fields=["average_rating"])


# =======================
# Inline
# =======================

class BookImageInline(admin.TabularInline):
    model = BookImage
    extra = 1


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    fields = ("user", "rating", "comment", "created_at")
    readonly_fields = ("user", "created_at")
    can_delete = True
    show_change_link = True


# =======================
# Admin Config
# =======================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

    #  CHO PHÉP SỬA / XOÁ RÕ RÀNG
    actions = ["delete_selected"]


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    actions = ["delete_selected"]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "author",
        "price",
        "sale_price",
        "stock",
        "average_rating",
        "created_at",
    )
    list_filter = ("category", "author", "created_at")
    search_fields = ("title", "author__name")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("price", "sale_price", "stock")
    date_hierarchy = "created_at"

    inlines = [BookImageInline, ReviewInline]

    readonly_fields = ("average_rating", "created_at", "updated_at")

    fieldsets = (
        ("Thông tin cơ bản", {
            "fields": ("title", "slug", "description", "category", "author")
        }),
        ("Giá & kho", {
            "fields": ("price", "sale_price", "stock")
        }),
        ("Đánh giá", {
            "fields": ("average_rating",)
        }),
        ("Thời gian", {
            "fields": ("created_at", "updated_at")
        }),
    )

    # CHO PHÉP XOÁ SÁCH (RÕ RÀNG)
    actions = ["delete_selected"]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("book", "user", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("book__title", "user__username")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
    actions = ["delete_selected"]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        update_book_average_rating(obj.book)

    def delete_model(self, request, obj):
        book = obj.book
        super().delete_model(request, obj)
        update_book_average_rating(book)

    def delete_queryset(self, request, queryset):
        books = set(obj.book for obj in queryset)
        super().delete_queryset(request, queryset)
        for book in books:
            update_book_average_rating(book)


@admin.register(ProductDiscount)
class ProductDiscountAdmin(admin.ModelAdmin):
    list_display = (
        "book",
        "discount_percent",
        "discount_amount",
        "is_active",
        "get_final_price",
    )
    list_filter = ("is_active",)
    search_fields = ("book__title",)
    actions = ["delete_selected"]

    def get_final_price(self, obj):
        return obj.get_discount_price()

    get_final_price.short_description = "Giá sau giảm"


@admin.register(BookViewHistory)
class BookViewHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "viewed_at")
    list_filter = ("viewed_at",)
    search_fields = ("user__username", "book__title")
    readonly_fields = ("user", "book", "viewed_at")
    ordering = ("-viewed_at",)
    actions = ["delete_selected"]


@admin.register(FavoriteBook)
class FavoriteBookAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "created_at")
    search_fields = ("user__username", "book__title")
    readonly_fields = ("created_at",)
    actions = ["delete_selected"]


@admin.register(RecommendationCache)
class RecommendationCacheAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "score", "updated_at")
    list_filter = ("updated_at",)
    search_fields = ("user__username", "book__title")
    ordering = ("-score",)
    actions = ["delete_selected"]
