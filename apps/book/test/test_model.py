from django.test import TestCase
from apps.book.models import Book, Category
from apps.user.models import User


class BookModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Khoa học")
        self.book = Book.objects.create(
            title="Vũ trụ",
            price=75000,
            author="Stephen Hawking",
            category=self.category
        )

    def test_category_to_string(self):
        print("\n--- Category __str__ ---")
        print(str(self.category))
        self.assertEqual(str(self.category), "Khoa học")

    def test_book_to_string(self):
        print("\n--- Book __str__ ---")
        print(str(self.book))
        self.assertEqual(str(self.book), "Vũ trụ")

    def test_book_fields(self):
        print("\n--- Book fields ---")
        print("Name:", self.book.title)
        print("Price:", self.book.price)
        print("Author:", self.book.author)
        print("Category:", self.book.category.name)

        self.assertEqual(self.book.price, 75000)
        self.assertEqual(self.book.category.name, "Khoa học")
