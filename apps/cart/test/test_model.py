from django.test import TestCase
from apps.user.models import User
from apps.book.models import Book
from apps.cart.models import Cart, CartItem

class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="hau", password="123")
        self.book = Book.objects.create(title="Sách A", price=50000)
        self.cart = Cart.objects.create(user=self.user)
        self.item = CartItem.objects.create(cart=self.cart, book=self.book, quantity=2)

    def test_cart_to_string(self):
        print("\n--- Cart __str__ ---")
        print(str(self.cart))
        self.assertEqual(str(self.cart), "Giỏ hàng của hau")

    def test_cart_total_price(self):
        print("\n--- Cart total price ---")
        print(self.cart.formatted_total_price())
        self.assertEqual(self.cart.formatted_total_price(), "100.000 ₫")

    def test_cart_item_to_string(self):
        print("\n--- CartItem __str__ ---")
        print(str(self.item))
        self.assertEqual(str(self.item), "Sách A (2)")

    def test_cart_item_total(self):
        print("\n--- CartItem total ---")
        print(self.item.get_total_price())
        self.assertEqual(self.item.get_total_price(), 100000)
