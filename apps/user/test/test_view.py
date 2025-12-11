from django.test import TestCase, Client
from django.urls import reverse
from apps.user.models import User


class UserViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="hau",
            password="123456"
        )

    def test_login_view(self):
        response = self.client.post(reverse("login"), {
            "username": "hau",
            "password": "123456"
        })

        print("\n--- Login status ---")
        print(response.status_code)

        self.assertEqual(response.status_code, 302)   # redirect thành công

    def test_profile_view_requires_login(self):
        response = self.client.get(reverse("profile"))
        print("\n--- Profile without login ---")
        print(response.status_code)
        self.assertEqual(response.status_code, 302)  # redirect login

    def test_profile_view_logged_in(self):
        self.client.login(username="hau", password="123456")
        response = self.client.get(reverse("profile"))

        print("\n--- Profile logged in ---")
        print(response.status_code)

        self.assertEqual(response.status_code, 200)
