# apps/order/models.py
from django.db import models
from decimal import Decimal
from django.utils import timezone

from apps.book.models import Book

# ======================================================
# 1 Promotion (KIỂU CŨ – có thể giữ để tham khảo)
# ======================================================
class Promotion(models.Model):
    """
    Mã khuyến mãi đơn giản (cũ)
    -> Có thể dùng cho demo hoặc legacy
    """
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.PositiveIntegerField(help_text="Phần trăm giảm (0-100)")
    expire_date = models.DateField()

    def __str__(self):
        return f"{self.code} ({self.discount_percent}%)"


# ======================================================
# 2 Voucher – PHIẾU GIẢM GIÁ (ADMIN TẠO)
# ======================================================
class Voucher(models.Model):
    """
    Voucher do ADMIN tạo (giống Shopee)
    User có thể lưu vào ví và dùng khi checkout
    """

    VOUCHER_TYPE = [
        ("PERCENT", "Giảm theo %"),
        ("FIXED", "Giảm tiền cố định"),
    ]

    name = models.CharField(max_length=100)  # Tên hiển thị
    voucher_type = models.CharField(max_length=10, choices=VOUCHER_TYPE)

    discount_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Giá trị giảm (% hoặc số tiền)"
    )

    min_order_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Đơn hàng tối thiểu để áp dụng"
    )

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    quantity = models.PositiveIntegerField(default=0, help_text="Số lượt sử dụng còn lại")
    is_active = models.BooleanField(default=True)

    def is_valid(self):
        """Kiểm tra voucher còn hợp lệ không"""
        now = timezone.now()
        return (
            self.is_active
            and self.start_date <= now <= self.end_date
            and self.quantity > 0
        )

    def __str__(self):
        return self.name


# ======================================================
# 3 UserVoucher – VÍ GIẢM GIÁ CỦA USER
# ======================================================
class UserVoucher(models.Model):
    """
    Liên kết USER – VOUCHER
    -> Đây chính là 'ví voucher' của user
    """

    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='user_vouchers'
    )

    voucher = models.ForeignKey(
        Voucher,
        on_delete=models.CASCADE,
        related_name='claimed_users'
    )

    used = models.BooleanField(default=False)  # Đã dùng hay chưa
    claimed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "voucher")

    def __str__(self):
        return f"{self.user.username} - {self.voucher.name}"


# ======================================================
# 4 Order – ĐƠN HÀNG
# ======================================================
class Order(models.Model):
    """
    Đơn hàng chính
    """

    STATUS_CHOICES = [
        ('Pending', 'Đang xử lý'),
        ('Shipped', 'Đang giao'),
        ('Completed', 'Hoàn thành'),
        ('Cancelled', 'Đã hủy'),
    ]

    PAYMENT_CHOICES = [
        ("COD", "Thanh toán khi nhận hàng"),
        ("BANK", "Chuyển khoản ngân hàng"),
    ]

    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='orders'
    )

    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_CHOICES,
        default="COD"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    shipping_address = models.TextField(blank=True, null=True)

    # ===== LIÊN KẾT GIẢM GIÁ =====
    user_voucher = models.ForeignKey(
        UserVoucher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Voucher user đã chọn"
    )

    promo_code = models.ForeignKey(
        'PromoCode',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Mã nhập tay"
    )

    # ===== GIÁ TIỀN =====
    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Tổng tiền gốc"
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Tổng tiền sau giảm"
    )

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


# ======================================================
# 5 OrderItem – CHI TIẾT SẢN PHẨM
# ======================================================
class OrderItem(models.Model):
    """
    Chi tiết từng sản phẩm trong đơn hàng
    """

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    book = models.ForeignKey('book.Book', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Giá tại thời điểm mua"
    )

    def __str__(self):
        return f"{self.book.title} x {self.quantity}"

    def get_total_price(self):
        return (self.price or Decimal('0.00')) * self.quantity


# ======================================================
# 6 RecommendationEngine – GỢI Ý SẢN PHẨM
# ======================================================
class RecommendationEngine(models.Model):
    """
    Lưu lịch sử mua hàng để gợi ý sách
    """

    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='recommendation_engines'
    )

    order_history = models.ManyToManyField(
        'book.Book',
        blank=True,
        related_name='recommended_in'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recommendations for {self.user.username}"

    def suggest_books(self, top_k=5):
        bought_ids = self.order_history.values_list('id', flat=True)
        return Book.objects.exclude(id__in=bought_ids)[:top_k]


# ======================================================
# 7 PromoCode – NHẬP MÃ BẰNG TAY
# ======================================================
class PromoCode(models.Model):
    """
    Mã giảm giá nhập tay (không lưu ví)
    """

    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.IntegerField(default=0)
    discount_amount = models.IntegerField(default=0)
    min_order_amount = models.IntegerField(default=0)

    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
