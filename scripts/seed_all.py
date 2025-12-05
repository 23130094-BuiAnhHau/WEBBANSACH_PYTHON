from apps.book.seed import run as seed_books
from apps.user.seed import run as seed_users
from apps.order.seed import run as seed_orders
from apps.cart.seed import run as seed_carts

# Script tổng hợp seed_all.py
# Mục đích: Xóa toàn bộ dữ liệu cũ (nếu cần) và tạo lại dữ liệu mẫu
# cho toàn bộ hệ thống BookStore (User, Book, Cart, Order, Promotion, v.v.)

def run(clear=True):
    """
    Hàm chính để seed toàn bộ dữ liệu hệ thống.
    
    Cách dùng trong Django shell:
        from scripts.seed_all import run

        run(clear=True)   # Xóa hết dữ liệu cũ và seed lại từ đầu
        run(clear=False)  # Giữ dữ liệu cũ, chỉ thêm dữ liệu mới
    """
    from apps.order.models import Order, OrderItem, Promotion
    from apps.cart.models import Cart, CartItem
    from apps.book.models import Book, Category
    from apps.user.models import User

    if clear:
        print("Đang xoá dữ liệu cũ...")

        # Xóa theo thứ tự đúng để tránh lỗi khóa ngoại (ForeignKey)
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Promotion.objects.all().delete()
        CartItem.objects.all().delete()
        Cart.objects.all().delete()
        Book.objects.all().delete()
        Category.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()  # Giữ lại tài khoản admin hệ thống

        print("Đã xoá toàn bộ dữ liệu cũ!\n")

    print("Bắt đầu tạo dữ liệu mới...")

    # Gọi lần lượt các file seed.py trong từng app
    seed_users()   # Tạo dữ liệu mẫu cho User (người dùng)
    seed_books()   # Tạo Category + Book + Review
    seed_carts()   # Tạo Cart và CartItem cho từng user
    seed_orders()  # Tạo Order, OrderItem, Promotion, RecommendationEngine

    print("\nSeed tất cả dữ liệu hoàn tất!")
