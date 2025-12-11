from django.test import TestCase, Client
from django.urls import reverse
from apps.user.models import User
from apps.book.models import Book
from apps.cart.models import Cart, CartItem
from apps.order.models import Order

class OrderViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="hau", password="123456")
        self.book = Book.objects.create(title="Sách A", price=60000)
        self.client.login(username="hau", password="123456")

        # Tạo giỏ có sản phẩm
        self.cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=self.cart, book=self.book, quantity=2)

    def test_checkout_without_promo(self):
        response = self.client.post(reverse("checkout"), {"promo_code": ""})
        self.assertEqual(response.status_code, 302)

        order = Order.objects.first()
        print("\n--- Checkout total amount ---")
        print(order.total_amount)

        self.assertEqual(order.total_amount, 120000)

    def test_order_history(self):
        Order.objects.create(user=self.user, total_price=10000, total_amount=8000)
        response = self.client.get(reverse("order_history"))
        print("\n--- Order history status ---")
        print(response.status_code)
        self.assertEqual(response.status_code, 200)
