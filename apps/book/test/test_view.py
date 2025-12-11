from django.test import TestCase, Client
from django.urls import reverse
from apps.book.models import Book, Category
from apps.user.models import User


class BookViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="hau", password="123456")

        self.category = Category.objects.create(name="Tiểu thuyết")
        self.book = Book.objects.create(
            title="Đắc nhân tâm",
            price=89000,
            author="Dale Carnegie",
            category=self.category
        )

    def test_book_list(self):
        response = self.client.get(reverse("book_list"))
        print("\n--- Book list view ---")
        print(response.status_code)
        self.assertEqual(response.status_code, 200)

    def test_book_detail(self):
        response = self.client.get(reverse("book_detail", args=[self.book.id]))
        print("\n--- Book detail view ---")
        print(response.status_code)
        self.assertEqual(response.status_code, 200)

    def test_add_review_requires_login(self):
        response = self.client.post(reverse("add_review", args=[self.book.id]), {
            "rating": 5,
            "comment": "Hay!"
        })
        print("\n--- Add review without login ---")
        print(response.status_code)

        self.assertEqual(response.status_code, 302)  # redirect login

    def test_add_review_success(self):
        self.client.login(username="hau", password="123456")

        response = self.client.post(reverse("add_review", args=[self.book.id]), {
            "rating": 5,
            "comment": "Tuyệt vời!"
        })

        print("\n--- Add review logged in ---")
        print(response.status_code)

        self.assertEqual(response.status_code, 302)
