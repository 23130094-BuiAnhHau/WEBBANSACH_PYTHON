from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return f"{self.username} ({self.role})"

    def is_admin_user(self):
        return self.role == 'admin'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=10,
        choices=[('Nam', 'Nam'), ('Nữ', 'Nữ'), ('Khác', 'Khác')],
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Hồ sơ {self.user.username}"


# Khuyến mãi theo khách hàng
class CustomerPromotion(models.Model):
    TYPE_CHOICES = [
        ("NEW", "Khách hàng mới"),
        ("VIP", "Khách hàng VIP"),
        ("BIRTHDAY", "Sinh nhật"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    promo_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    discount_percent = models.PositiveIntegerField(default=0)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def is_valid(self):
        now = timezone.now()
        return self.is_active and self.start_date <= now <= self.end_date

    def __str__(self):
        return f"{self.user.username} - {self.promo_type} ({self.discount_percent}%)"
