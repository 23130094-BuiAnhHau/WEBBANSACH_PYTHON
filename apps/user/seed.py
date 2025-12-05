from faker import Faker # type: ignore
from apps.user.models import User, Profile
from datetime import date, timedelta
import random

fake = Faker("vi_VN")

def run(clear=False):
    """Seed dữ liệu User và Profile"""
    if clear:
        print("Xoá dữ liệu User cũ...")
        User.objects.all().delete()

    print("Tạo admin...")
    admin = User.objects.create_superuser(
        username="admin",
        email="admin@bookstore.com",
        password="123456",
        role="admin",
        is_admin=True,
        is_customer=False
    )

    print("Tạo 20 user thường...")
    users = []
    for _ in range(20):
        user = User.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            phone=fake.phone_number(),
            address=fake.address(),
            role="user",
            is_admin=False,
            is_customer=True
        )
        user.date_joined = date.today() - timedelta(days=random.randint(400, 1200))
        user.set_password("123456")
        user.save()

        Profile.objects.create(
            user=user,
            gender=random.choice(["Nam","Nữ","Khác"]),
            date_of_birth=date.today() - timedelta(days=random.randint(7000, 15000))
        )
        users.append(user)

    print(f"Đã tạo {len(users)} user và 1 admin")
