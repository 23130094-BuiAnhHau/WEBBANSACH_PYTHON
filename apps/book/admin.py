from django.contrib import admin
from .models import (
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

# =======================
# Inline
# =======================

class BookImageInline(admin.TabularInline):
    model = BookImage
    extra = 1


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ("user", "rating", "created_at")
    can_delete = False


# =======================
# Admin Config
# =======================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


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


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("book", "user", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("book__title", "user__username")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)


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


@admin.register(FavoriteBook)
class FavoriteBookAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "created_at")
    search_fields = ("user__username", "book__title")
    readonly_fields = ("created_at",)


@admin.register(RecommendationCache)
class RecommendationCacheAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "score", "updated_at")
    list_filter = ("updated_at",)
    search_fields = ("user__username", "book__title")
    ordering = ("-score",)
