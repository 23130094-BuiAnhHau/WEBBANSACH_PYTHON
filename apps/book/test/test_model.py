from django.test import TestCase
from apps.book.models import Book, Category

class BookModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Cate")
        self.book = Book.objects.create(
            title="Book A",
            author="Author",
            price=50000,
            category=self.category
        )

    def test_category_to_string(self):
        print("\n--- Category __str__ ---")
        print(str(self.category))
        self.assertEqual(str(self.category), "Test Cate")

    def test_book_to_string(self):
        print("\n--- Book __str__ ---")
        print(str(self.book))
        self.assertEqual(str(self.book), "Book A - Author")

    def test_book_fields(self):
        print("\n--- Book fields ---")
        print("Name:", self.book.title)
        print("Price:", self.book.price)
        print("Author:", self.book.author)
        print("Category:", self.book.category.name)

        self.assertEqual(self.book.title, "Book A")
        self.assertEqual(self.book.price, 50000)
        self.assertEqual(self.book.author, "Author")
        self.assertEqual(self.book.category.name, "Test Cate")
