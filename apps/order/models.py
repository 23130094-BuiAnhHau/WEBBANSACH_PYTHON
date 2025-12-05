from django.db import models
from BookStore.utils.format_currency import format_currency_vnd

# Đơn hàng
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Đang xử lý'),
        ('Shipped', 'Đã giao'),
        ('Completed', 'Hoàn thành'),
        ('Cancelled', 'Đã hủy'),
    ]

    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='orders'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    shipping_address = models.TextField(blank=True, null=True)

    # Tổng thanh toán sau khuyến mãi
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    promotion = models.ForeignKey(
        'Promotion',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Đơn hàng #{self.id} của {self.user.username}"

    

# Chi tiết sản phẩm trong đơn hàng
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    book = models.ForeignKey('book.Book', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.book.title} x {self.quantity}"

    def get_total_price(self):
        return self.price * self.quantity


# Mã khuyến mãi
class Promotion(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_percent = models.PositiveIntegerField()  # Giảm %
    expire_date = models.DateField()

    def __str__(self):
        return f"{self.code} ({self.discount_percent}% đến {self.expire_date})"


# Hệ thống gợi ý sách
class RecommendationEngine(models.Model):
    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='recommendations'
    )
    order_history = models.ManyToManyField(
        'book.Book',
        related_name='recommended_in'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # Gợi ý sách chưa mua
    def suggest_books(self):
        return (
            self.order_history.model.objects
            .exclude(id__in=self.order_history.values_list('id', flat=True))
        )[:5]

    def __str__(self):
        return f"Recommendations for {self.user.username}"
