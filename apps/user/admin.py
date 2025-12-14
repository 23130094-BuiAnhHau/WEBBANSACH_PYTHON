from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, Profile, CustomerPromotion


# ======================================================
# Inline Profile
# ======================================================
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    extra = 0


# ======================================================
# User Admin
# ======================================================
@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = (
        "username",
        "email",
        "phone",
        "role",
        "is_active",
        "is_staff",
    )
    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("username", "email", "phone")
    ordering = ("username",)
    inlines = [ProfileInline]

    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Thông tin thêm", {
            "fields": ("phone", "address", "role")
        }),
    )

    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        ("Thông tin thêm", {
            "fields": ("phone", "address", "role")
        }),
    )


# ======================================================
# Profile (xem lẻ – ít dùng)
# ======================================================
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "date_of_birth", "gender")
    search_fields = ("user__username",)
    list_filter = ("gender",)


# ======================================================
# CustomerPromotion – Khuyến mãi theo khách hàng
# ======================================================
@admin.register(CustomerPromotion)
class CustomerPromotionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "promo_type",
        "discount_percent",
        "is_active",
        "start_date",
        "end_date",
    )
    list_filter = ("promo_type", "is_active")
    search_fields = ("user__username",)
    ordering = ("-start_date",)
