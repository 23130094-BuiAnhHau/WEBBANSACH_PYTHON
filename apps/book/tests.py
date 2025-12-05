from django.test import TestCase, Client
from apps.book.models import Book, Category

class BookViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Văn học")
        self.book = Book.objects.create(
            title="Sách Test",
            author="Tác giả Test",
            price=100000,
            category=self.category,
            stock=10
        )

    def test_book_list(self):
        response = self.client.get("/books/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sách Test")

    def test_book_detail(self):
        response = self.client.get(f"/books/{self.book.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tác giả Test")
