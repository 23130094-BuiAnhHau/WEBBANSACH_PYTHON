from django.test import TestCase
from apps.user.models import User
from apps.book.models import Book
from apps.order.models import Order, OrderItem, Promotion
from datetime import date

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="hau", password="123")
        self.book = Book.objects.create(title="Sách A", price=60000)
        self.promo = Promotion.objects.create(
            code="SALE20",
            discount_percent=20,
            expire_date=date.today()
        )
        self.order = Order.objects.create(
            user=self.user,
            total_price=0,
            total_amount=0,
            promotion=self.promo
        )
        self.item = OrderItem.objects.create(
            order=self.order,
            book=self.book,
            price=60000,
            quantity=3
        )

    def test_order_to_string(self):
        print("\n--- Order __str__ ---")
        print(str(self.order))
        self.assertIn("Đơn hàng #", str(self.order))

    def test_order_item_total(self):
        total = self.item.get_total_price()
        print("\n--- Order item total ---")
        print(total)
        self.assertEqual(total, 180000)

    def test_promotion_to_string(self):
        print("\n--- Promotion __str__ ---")
        print(str(self.promo))
        self.assertIn("SALE20", str(self.promo))
