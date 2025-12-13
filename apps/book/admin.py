from django.contrib import admin
from .models import Book, Category, Author, BookImage, Review

class BookImageInline(admin.TabularInline):
    model = BookImage
    extra = 1

class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "author", "price", "stock")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [BookImageInline]

admin.site.register(Book, BookAdmin)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Review)
