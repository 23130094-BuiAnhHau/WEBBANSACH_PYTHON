from django.db import models

class Cart(models.Model):
    user = models.OneToOneField('user.User', on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    def total_price(self):
        return sum(item.get_total_price() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey('book.Book', on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.book} x {self.quantity}"

    def get_total_price(self):
        if not self.book:
            return 0
        return self.book.price * self.quantity
