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
# OrderItem – Chi tiết đơn hàng
# ======================================================
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'order',
        'book',
        'quantity',
        'formatted_price',
        'formatted_total_price'
    )
    readonly_fields = ('formatted_price', 'formatted_total_price')
    search_fields = ('book__title', 'order__user__username')

    def formatted_price(self, obj):
        return format_currency_vnd(obj.price)
    formatted_price.short_description = "Giá (VNĐ)"

    def formatted_total_price(self, obj):
        return format_currency_vnd(obj.get_total_price())
    formatted_total_price.short_description = "Thành tiền (VNĐ)"


# ======================================================
# Order – Đơn hàng
# ======================================================
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'status',
        'payment_method',
        'voucher_display',
        'promo_code',
        'formatted_total_amount',
        'created_at'
    )

    list_filter = ('status', 'created_at', 'payment_method')
    search_fields = ('user__username',)
    readonly_fields = ('formatted_total_amount',)

    def formatted_total_amount(self, obj):
        return format_currency_vnd(obj.total_amount)
    formatted_total_amount.short_description = "Tổng thanh toán (VNĐ)"

    def voucher_display(self, obj):
        if obj.user_voucher:
            return obj.user_voucher.voucher.name
        return "-"
    voucher_display.short_description = "Voucher áp dụng"


# ======================================================
# Promotion (cũ – nếu còn dùng)
# ======================================================
@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'expire_date')
    search_fields = ('code',)


# ======================================================
# Voucher – Phiếu giảm giá (Admin tạo)
# ======================================================
@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'voucher_type',
        'discount_value',
        'min_order_amount',
        'quantity',
        'is_active',
        'start_date',
        'end_date'
    )
    list_filter = ('voucher_type', 'is_active')
    search_fields = ('name',)


# ======================================================
# UserVoucher – Ví voucher của user
# ======================================================
@admin.register(UserVoucher)
class UserVoucherAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'voucher',
        'used',
        'claimed_at'
    )
    list_filter = ('used',)
    search_fields = ('user__username', 'voucher__name')


# ======================================================
# PromoCode – Mã nhập tay
# ======================================================
@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'discount_percent',
        'discount_amount',
        'min_order_amount',
        'is_active',
        'valid_from',
        'valid_to'
    )
    list_filter = ('is_active',)
    search_fields = ('code',)


# ======================================================
# RecommendationEngine – Gợi ý
# ======================================================
@admin.register(RecommendationEngine)
class RecommendationEngineAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    filter_horizontal = ('order_history',)
