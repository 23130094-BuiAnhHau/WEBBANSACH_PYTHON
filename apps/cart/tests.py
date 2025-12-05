from django.test import TestCase, Client
from apps.user.models import User
from apps.book.models import Book
from apps.cart.models import Cart

class CartViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="user", password="123")
        self.book = Book.objects.create(title="Sách A", author="Tác giả", price=100, stock=10, category_id=1)

    def test_add_to_cart(self):
        self.client.login(username="user", password="123")
        response = self.client.get(f"/cart/add/{self.book.id}/")
        self.assertEqual(response.status_code, 302)  # redirect về cart_detail
