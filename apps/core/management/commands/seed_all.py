from django.core.management.base import BaseCommand
from apps.user.seed import run as seed_users
from apps.book.seed import run as seed_books
from apps.order.seed import run as seed_orders

class Command(BaseCommand):
    help = "Seed fake data for all apps"

    def handle(self, *args, **kwargs):
        self.stdout.write(" Xóa dữ liệu cũ...")
        # tuỳ muốn xoá bảng nào trước
        seed_users(clear=True)
        seed_books(clear=True)
        seed_orders(clear=True)

        self.stdout.write(" Tạo dữ liệu mới...")
        seed_users()
        seed_books()
        seed_orders()

        self.stdout.write(self.style.SUCCESS("Done seeding all fake data!"))
from apps.book.seed import run as seed_books
from apps.user.seed import run as seed_users
from apps.order.seed import run as seed_orders
from apps.cart.seed import run as seed_carts


def run(clear=True):
    """
    Xóa dữ liệu cũ và seed lại toàn bộ hệ thống BookStore.
    Dùng:
        from scripts.seed_all import run
        run(clear=True)  # Xóa hết và tạo lại
        run(clear=False) # Chỉ thêm dữ liệu mới
    """
    from apps.order.models import Order, OrderItem, Promotion
    from apps.cart.models import Cart, CartItem
    from apps.book.models import Book, Category
    from apps.user.models import User

    if clear:
        print(" Đang xoá dữ liệu cũ...")

        # Xóa theo thứ tự tránh lỗi khoá ngoại
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Promotion.objects.all().delete()
        CartItem.objects.all().delete()
        Cart.objects.all().delete()
        Book.objects.all().delete()
        Category.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

        print(" Đã xoá toàn bộ dữ liệu cũ!\n")

    print(" Bắt đầu tạo dữ liệu mới...")

    # Gọi từng seed script (các file seed.py trong từng app)
    seed_users()
    seed_books()
    seed_carts()
    seed_orders()

    print("\n Seed tất cả dữ liệu hoàn tất!")
