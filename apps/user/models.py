from django.db import models
from django.contrib.auth.models import AbstractUser

# Người dùng kế thừa từ AbstractUser (tự có username, email, password…)
class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)   # Số điện thoại
    address = models.TextField(blank=True, null=True)                # Địa chỉ nhà
    is_customer = models.BooleanField(default=True)                  # Người dùng bình thường?
    is_admin = models.BooleanField(default=False)                    # Có phải admin hệ thống?

    # Vai trò hiển thị trong admin
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return self.username


# Hồ sơ người dùng (1 user -> 1 profile)
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
        return f"Hồ sơ của {self.user.username}"


# Tài khoản Admin kế thừa User
class Admin(User):
    class Meta:
        verbose_name = "Admin"
        verbose_name_plural = "Admins"

    # Ghi đè save để bắt buộc admin mang quyền admin
    def save(self, *args, **kwargs):
        self.role = 'admin'
        self.is_admin = True
        self.is_customer = False
        super().save(*args, **kwargs)
