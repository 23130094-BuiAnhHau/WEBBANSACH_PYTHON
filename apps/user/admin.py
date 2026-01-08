from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from apps.user.models import User, Profile



class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    extra = 0



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

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "date_of_birth", "gender")
    search_fields = ("user__username",)
    list_filter = ("gender",)



