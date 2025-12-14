from django.contrib import admin
from apps.cart.models import Cart, CartItem
from BookStore.utils.format_currency import format_currency_vnd


# =======================
# Inline CartItem
# =======================

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    can_delete = True
    readonly_fields = ("price_display", "total_price_display")
    fields = ("book", "quantity", "price_display", "total_price_display")

    def price_display(self, obj):
        return format_currency_vnd(obj.price)

    price_display.short_description = "Giá tại thời điểm thêm"

    def total_price_display(self, obj):
        return format_currency_vnd(obj.price * obj.quantity)

    total_price_display.short_description = "Thành tiền"


# =======================
# Cart Admin
# =======================

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "total_price_display", "created_at", "updated_at")
    search_fields = ("user__username", "user__email")
    readonly_fields = ("total_price_display", "created_at", "updated_at")
    inlines = [CartItemInline]
    ordering = ("-updated_at",)

    def total_price_display(self, obj):
        total = sum(item.price * item.quantity for item in obj.items.all())
        return format_currency_vnd(total)

    total_price_display.short_description = "Tổng tiền"


# =======================
# CartItem Admin
# =======================

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        "cart",
        "book",
        "quantity",
        "price_display",
        "total_price_display",
    )
    search_fields = ("book__title", "cart__user__username")
    list_filter = ("book",)
    readonly_fields = ("price_display", "total_price_display")

    def price_display(self, obj):
        return format_currency_vnd(obj.price)

    price_display.short_description = "Giá"

    def total_price_display(self, obj):
        return format_currency_vnd(obj.price * obj.quantity)

    total_price_display.short_description = "Thành tiền"
