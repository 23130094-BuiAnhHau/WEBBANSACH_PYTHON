from django.contrib import admin
from apps.cart.models import Cart, CartItem
from BookStore.utils.format_currency import format_currency_vnd


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('formatted_price', 'formatted_total_price')
    fields = ('book', 'quantity', 'formatted_price', 'formatted_total_price')

    def formatted_price(self, obj):
        return format_currency_vnd(obj.book.price if obj.book else 0)

    def formatted_total_price(self, obj):
        return format_currency_vnd((obj.book.price if obj.book else 0) * obj.quantity)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'formatted_total_price', 'created_at')
    readonly_fields = ('formatted_total_price',)
    inlines = [CartItemInline]

    def formatted_total_price(self, obj):
        total = sum(
            (item.book.price if item.book else 0) * item.quantity
            for item in obj.items.all()
        )
        return format_currency_vnd(total)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'book', 'quantity', 'formatted_price', 'formatted_total_price')
    readonly_fields = ('formatted_price', 'formatted_total_price')

    def formatted_price(self, obj):
        return format_currency_vnd(obj.book.price if obj.book else 0)

    def formatted_total_price(self, obj):
        return format_currency_vnd((obj.book.price if obj.book else 0) * obj.quantity)
