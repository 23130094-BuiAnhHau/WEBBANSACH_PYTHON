import random
from decimal import Decimal
from django.utils import timezone
from faker import Faker # type: ignore
from apps.book.models import Category, Book, Review
from apps.user.models import User

fake = Faker("vi_VN")

def run(clear=False):
    """Seed Category, Book và Review"""
    if clear:
        print("Xoá dữ liệu Category, Book, Review cũ...")
        Review.objects.all().delete()
        Book.objects.all().delete()
        Category.objects.all().delete()

    # Danh mục sách
    category_names = ["Văn học", "Kinh tế", "Tâm lý học", "Khoa học", "Thiếu nhi", "Công nghệ"]
    categories = [Category.objects.get_or_create(name=name)[0] for name in category_names]

    # Ảnh bìa mẫu
    cover_dir = "book_covers"
    sample_covers = [f"{cover_dir}/book{i}.jpg" for i in range(1,6)]

    # Tạo sách
    books = []
    for _ in range(30):
        title = fake.sentence(nb_words=random.randint(2,5)).replace(".", "").title()
        author = fake.name()
        description = fake.paragraph(nb_sentences=random.randint(2,4))
        price = Decimal(random.randint(60000, 350000))
        category = random.choice(categories)
        cover_image = random.choice(sample_covers)

        book, created = Book.objects.get_or_create(
            title=title,
            defaults={
                "author": author,
                "price": price,
                "description": description,
                "category": category,
                "stock": random.randint(5,50),
                "published_date": timezone.now().date(),
                "cover_image": cover_image
            }
        )
        if created:
            books.append(book)

    print(f"Đã tạo {len(books)} sách")

    # Tạo Review
    users = list(User.objects.all())
    if users and books:
        count = 0
        for user in users:
            for _ in range(random.randint(1,3)):
                Review.objects.create(
                    user=user,
                    book=random.choice(books),
                    rating=random.randint(3,5),
                    content=fake.paragraph(nb_sentences=2)
                )
                count += 1
        print(f"Đã tạo {count} review")
