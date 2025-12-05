from django.contrib import admin
from apps.cart.models import Cart, CartItem
from BookStore.utils.format_currency import format_currency_vnd

# --- Inline cho CartItem trong Cart ---
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('formatted_price', 'formatted_total_price')
    fields = ('book', 'quantity', 'formatted_price', 'formatted_total_price')

    # Method cho CartItemInline
    def formatted_price(self, obj):
        return format_currency_vnd(obj.price)
    formatted_price.short_description = "Giá (VNĐ)"

    def formatted_total_price(self, obj):
        return format_currency_vnd(obj.price * obj.quantity)
    formatted_total_price.short_description = "Tổng tiền (VNĐ)"

# --- Admin cho Cart ---
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'formatted_total_price', 'created_at')
    readonly_fields = ('formatted_total_price',)
    inlines = [CartItemInline]

    # Method cho CartAdmin
    def formatted_total_price(self, obj):
        total = sum(item.price * item.quantity for item in obj.cartitem_set.all())
        return format_currency_vnd(total)
    formatted_total_price.short_description = "Tổng tiền (VNĐ)"

# --- Admin cho CartItem riêng ---
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'book', 'quantity', 'formatted_price', 'formatted_total_price')
    readonly_fields = ('formatted_price', 'formatted_total_price')

    # Method cho CartItemAdmin
    def formatted_price(self, obj):
        return format_currency_vnd(obj.price)
    formatted_price.short_description = "Giá (VNĐ)"

    def formatted_total_price(self, obj):
        return format_currency_vnd(obj.price * obj.quantity)
    formatted_total_price.short_description = "Tổng tiền (VNĐ)"
