from django.contrib import admin
from apps.home.models import Banner
from django.utils.html import format_html

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("title", "subtitle", "is_active", "preview_image")
    list_filter = ("is_active",)
    search_fields = ("title", "subtitle")
    list_editable = ("is_active",)
    #Xem trức hình ảnh
    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:50px;"/>', obj.image)
        return "-"
    preview_image.short_description = "Hình ảnh"
