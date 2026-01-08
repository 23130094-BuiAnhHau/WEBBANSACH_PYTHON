from django.db import models
from django.core.validators import MinValueValidator

class Cart(models.Model):
    user = models.OneToOneField('user.User', on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    @property
    def total_price(self):
        return sum(item.get_total_price() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    book = models.ForeignKey(
    "book.Book",
    on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    def get_total_price(self):
        return self.book.get_final_price() * self.quantity
