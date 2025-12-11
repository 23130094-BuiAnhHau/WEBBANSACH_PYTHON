from django.test import TestCase, Client
from django.urls import reverse
from apps.user.models import User
from apps.book.models import Book
from apps.cart.models import CartItem

class CartViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="hau", password="123456")
        self.book = Book.objects.create(title="Sách A", price=50000)
        self.client.login(username="hau", password="123456")

    def test_cart_detail(self):
        response = self.client.get(reverse("cart_detail"))
        self.assertEqual(response.status_code, 200)

    def test_add_to_cart(self):
        response = self.client.get(reverse("add_to_cart", args=[self.book.id]))
        self.assertEqual(response.status_code, 302)

        item = CartItem.objects.first()
        print("\n--- Add to cart result ---")
        print(item.book.title, item.quantity)

        self.assertEqual(item.quantity, 1)

    def test_remove_from_cart(self):
        # Tạo item trước
        self.client.get(reverse("add_to_cart", args=[self.book.id]))
        item = CartItem.objects.first()

        response = self.client.get(reverse("remove_from_cart", args=[item.id]))
        self.assertEqual(response.status_code, 302)

        print("\n--- After remove, item count ---")
        print(CartItem.objects.count())

        self.assertEqual(CartItem.objects.count(), 0)
