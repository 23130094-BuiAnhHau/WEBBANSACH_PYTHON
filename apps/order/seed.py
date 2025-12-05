import random
from decimal import Decimal
from datetime import date, timedelta
from faker import Faker # type: ignore
from apps.order.models import Order, OrderItem, Promotion, RecommendationEngine
from apps.user.models import User
from apps.book.models import Book

fake = Faker("vi_VN")

def run(clear=False):
    """Seed dữ liệu Order, OrderItem, Promotion, RecommendationEngine"""
    if clear:
        print(" Xoá dữ liệu Order, OrderItem, Promotion, RecommendationEngine...")
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Promotion.objects.all().delete()
        RecommendationEngine.objects.all().delete()

    users = list(User.objects.all())
    books = list(Book.objects.all())
    if not users or not books:
        print("Cần có User và Book trước khi seed Order.")
        return

    # Tạo promotions
    promotions = []
    for _ in range(3):
        promo = Promotion.objects.create(
            code=fake.lexify(text="PROMO????"),
            discount_percent=random.choice([5,10,15,20,25]),
            expire_date=date.today() + timedelta(days=random.randint(10,100))
        )
        promotions.append(promo)

    # Tạo 20 đơn hàng
    for _ in range(20):
        user = random.choice(users)
        promo = random.choice(promotions + [None])
        order = Order.objects.create(user=user, promotion=promo, total_price=0, total_amount=0)

        total = Decimal(0)
        for book in random.sample(books, random.randint(1,3)):
            quantity = random.randint(1,3)
            item = OrderItem.objects.create(
                order=order,
                book=book,
                quantity=quantity,
                price=book.price
            )
            total += item.get_total_price()

        order.total_price = total
        order.total_amount = total * (1 - promo.discount_percent/100) if promo else total
        order.save()

    # RecommendationEngine
    for user in users:
        engine = RecommendationEngine.objects.create(user=user)
        history_books = random.sample(books, random.randint(2,5))
        engine.order_history.set(history_books)

    print(" Đã seed Orders, OrderItems, Promotion & RecommendationEngine")
