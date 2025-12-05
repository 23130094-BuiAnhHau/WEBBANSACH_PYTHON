from django.test import TestCase, Client
from apps.user.models import User
from apps.book.models import Book
from apps.cart.models import Cart, CartItem

class OrderViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="u1", password="123")
        self.book = Book.objects.create(title="B1", author="A", price=100, stock=10, category_id=1)
        self.cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=self.cart, book=self.book, quantity=1)

    def test_checkout(self):
        self.client.login(username="u1", password="123")
        response = self.client.post("/checkout/", {})
        self.assertEqual(response.status_code, 302)
