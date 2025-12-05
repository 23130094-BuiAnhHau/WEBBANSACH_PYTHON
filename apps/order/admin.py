from django.contrib import admin
from .models import Order, OrderItem, Promotion, RecommendationEngine
from BookStore.utils.format_currency import format_currency_vnd

# --- Admin cho OrderItem ---
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'book', 'quantity', 'formatted_price', 'formatted_total_price')
    list_filter = ('order__status',)
    search_fields = ('book__title', 'order__user__username')
    readonly_fields = ('formatted_price', 'formatted_total_price')

    def formatted_price(self, obj):
        return format_currency_vnd(obj.price)
    formatted_price.short_description = "Giá (VNĐ)"

    def formatted_total_price(self, obj):
        return format_currency_vnd(obj.price * obj.quantity)
    formatted_total_price.short_description = "Tổng tiền (VNĐ)"

# --- Admin cho Order ---
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'formatted_total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)
    readonly_fields = ('formatted_total_price',)

    def formatted_total_price(self, obj):
        total = sum(item.price * item.quantity for item in obj.orderitem_set.all())
        return format_currency_vnd(total)
    formatted_total_price.short_description = "Tổng tiền (VNĐ)"

# --- Admin cho Promotion ---
@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'expire_date')
    search_fields = ('code',)

# --- Admin cho RecommendationEngine ---
@admin.register(RecommendationEngine)
class RecommendationEngineAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    filter_horizontal = ('order_history',)
