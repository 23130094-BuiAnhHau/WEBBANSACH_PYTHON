from django.db import models

# Giỏ hàng của user (1 user -> 1 giỏ)
class Cart(models.Model):
    user = models.OneToOneField(
        'user.User',
        on_delete=models.CASCADE,
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Giỏ hàng của {self.user.username}"

    # Tính tổng tiền trong giỏ
    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    def formatted_total_price(self):
        total = self.total_price
        return f"{int(total):,} ₫".replace(",", ".")
    formatted_total_price.short_description = "Tổng tiền (VNĐ)"


# Một mục trong giỏ (CartItem)
class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'   # 1 giỏ -> nhiều item
    )
    book = models.ForeignKey(
        'book.Book',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.book.title} ({self.quantity})"

    # Giá 1 sản phẩm
    @property
    def price(self):
        return self.book.price

    # Tổng giá = giá * số lượng
    @property
    def total_price(self):
        return self.price * self.quantity

    def formatted_price(self):
        return f"{int(self.price):,} ₫".replace(",", ".")
    formatted_price.short_description = "Giá (VNĐ)"

    def formatted_total_price(self):
        return f"{int(self.total_price):,} ₫".replace(",", ".")
    formatted_total_price.short_description = "Thành tiền (VNĐ)"
