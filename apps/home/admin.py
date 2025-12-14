from django.contrib import admin

from apps.home.model import Banner



@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("title", "subtitle", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "subtitle")
    list_editable = ("is_active",)
