from django.contrib import admin
from .models import (
    Order,
    OrderItem,
    Promotion,
    RecommendationEngine,
    Voucher,
    UserVoucher,
    PromoCode,
)
from BookStore.utils.format_currency import format_currency_vnd


# ======================================================
# Inline: OrderItem
# ======================================================
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    readonly_fields = ("price_display", "total_price_display")
    fields = ("book", "quantity", "price_display", "total_price_display")

    def price_display(self, obj):
        return format_currency_vnd(obj.price)

    price_display.short_description = "Giá mua"

    def total_price_display(self, obj):
        return format_currency_vnd(obj.get_total_price())

    total_price_display.short_description = "Thành tiền"


# ======================================================
# Order – Đơn hàng
# ======================================================
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "status",
        "payment_method",
        "voucher_display",
        "promo_code",
        "total_amount_display",
        "created_at",
    )
    list_filter = ("status", "payment_method", "created_at")
    search_fields = ("user__username", "user__email")
    ordering = ("-created_at",)
    inlines = [OrderItemInline]

    readonly_fields = (
        "total_price_display",
        "total_amount_display",
        "created_at",
    )

    fieldsets = (
        ("Thông tin đơn hàng", {
            "fields": ("user", "status", "payment_method", "shipping_address")
        }),
        ("Giảm giá", {
            "fields": ("user_voucher", "promo_code")
        }),
        ("Giá tiền", {
            "fields": ("total_price_display", "total_amount_display")
        }),
        ("Thời gian", {
            "fields": ("created_at",)
        }),
    )

    def total_price_display(self, obj):
        return format_currency_vnd(obj.total_price)

    total_price_display.short_description = "Tổng tiền gốc"

    def total_amount_display(self, obj):
        return format_currency_vnd(obj.total_amount)

    total_amount_display.short_description = "Tổng thanh toán"

    def voucher_display(self, obj):
        if obj.user_voucher:
            return obj.user_voucher.voucher.name
        return "-"

    voucher_display.short_description = "Voucher"


# ======================================================
# OrderItem (xem lẻ – ít dùng)
# ======================================================
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "book",
        "quantity",
        "price_display",
        "total_price_display",
    )
    search_fields = ("book__title", "order__user__username")
    readonly_fields = ("price_display", "total_price_display")

    def price_display(self, obj):
        return format_currency_vnd(obj.price)

    def total_price_display(self, obj):
        return format_currency_vnd(obj.get_total_price())


# ======================================================
# Promotion (CŨ – demo)
# ======================================================
@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ("code", "discount_percent", "expire_date")
    search_fields = ("code",)


# ======================================================
# Voucher – ADMIN tạo
# ======================================================
@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "voucher_type",
        "discount_value",
        "min_order_amount",
        "quantity",
        "is_active",
        "start_date",
        "end_date",
    )
    list_filter = ("voucher_type", "is_active")
    search_fields = ("name",)
    ordering = ("-start_date",)


# ======================================================
# UserVoucher – Ví của user
# ======================================================
@admin.register(UserVoucher)
class UserVoucherAdmin(admin.ModelAdmin):
    list_display = ("user", "voucher", "used", "claimed_at")
    list_filter = ("used",)
    search_fields = ("user__username", "voucher__name")
    readonly_fields = ("claimed_at",)


# ======================================================
# PromoCode – Nhập tay
# ======================================================
@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "discount_percent",
        "discount_amount",
        "min_order_amount",
        "is_active",
        "valid_from",
        "valid_to",
    )
    list_filter = ("is_active",)
    search_fields = ("code",)


# ======================================================
# RecommendationEngine – AI
# ======================================================
@admin.register(RecommendationEngine)
class RecommendationEngineAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")
    filter_horizontal = ("order_history",)
    readonly_fields = ("created_at",)
