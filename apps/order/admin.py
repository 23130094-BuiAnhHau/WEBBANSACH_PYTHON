from django.contrib import admin
from .models import (
    Promotion,
    Voucher,
    UserVoucher,
    Order,
    OrderItem,
    PromoCode,
    RecommendationEngine,
)

# Promotio
@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ("code", "discount_percent", "expire_date")
    search_fields = ("code",)
    list_filter = ("expire_date",)



# Voucher (admin tạo)
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



# UserVoucher (ví voucher
@admin.register(UserVoucher)
class UserVoucherAdmin(admin.ModelAdmin):
    list_display = ("user", "voucher", "used", "claimed_at")
    list_filter = ("used",)
    search_fields = ("user__username", "voucher__name")



# OrderItem (inline)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("book", "price", "quantity")



# Order (đơn hàng)
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "payment_method",
        "status",
        "total_amount",
        "created_at",
    )
    list_filter = ("status", "payment_method", "created_at")
    search_fields = ("id", "user__username")
    readonly_fields = ("created_at",)
    inlines = [OrderItemInline]

    actions = [
        "mark_completed",
        "mark_cancelled",
    ]

    # Đánh dấu hoàn thành
    @admin.action(description="Đánh dấu đơn hàng đã hoàn thành")
    def mark_completed(self, request, queryset):
        queryset.update(status="Completed")

    # Đánh dấu huỷ
    @admin.action(description="Huỷ đơn hàng")
    def mark_cancelled(self, request, queryset):
        queryset.update(status="Cancelled")

# PromoCode (nhập tay)

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

# Recommendation Engine

@admin.register(RecommendationEngine)
class RecommendationEngineAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")
    search_fields = ("user__username",)
