from django.contrib import admin
from .models import Book, Category, Review
from django.utils.html import format_html

# Đăng ký model Book với trang quản trị Django
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Các cột hiển thị trong danh sách Book
    list_display = ('title', 'author', 'formatted_price', 'display_cover')

    def display_cover(self, obj):
        """
        Hiển thị ảnh bìa thu nhỏ trong trang admin.
        Nếu không có ảnh -> trả về text "(Không có ảnh)"
        """
        try:
            if obj.cover_image and hasattr(obj.cover_image, 'url'):
                return format_html(
                    '<img src="{}" width="60" style="border-radius:6px; box-shadow:0 0 4px #ccc;" />',
                    obj.cover_image.url
                )
        except Exception:
            pass
        return "(Không có ảnh)"

# Quản lý phần đánh giá sách trong trang admin
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'created_at')     # Hiển thị thông tin chính của review
    list_filter = ('rating', 'created_at')      # Bộ lọc theo điểm đánh giá và ngày tạo
    search_fields = ('book__title', 'user__username', 'content')        # Cho phép tìm kiếm theo tên sách, username và nội dung

# Quản lý danh mục sách trong admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)        # Chỉ hiển thị tên danh mục
