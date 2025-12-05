import random
from apps.cart.models import Cart, CartItem
from apps.user.models import User
from apps.book.models import Book

def run(clear=False):
    """Seed dữ liệu Cart & CartItem"""
    if clear:
        print("Xoá dữ liệu Cart & CartItem cũ...")
        CartItem.objects.all().delete()
        Cart.objects.all().delete()

    users = list(User.objects.all())
    books = list(Book.objects.all())
    if not users or not books:
        print("Thiếu User hoặc Book để tạo giỏ hàng.")
        return

    for user in users:
        cart = Cart.objects.create(user=user)
        for book in random.sample(books, min(3, len(books))):
            CartItem.objects.create(
                cart=cart,
                book=book,
                quantity=random.randint(1,4)
            )

    print(f"Đã tạo giỏ hàng cho {len(users)} khách hàng")
