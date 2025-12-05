from django.test import TestCase, Client
from apps.user.models import User

class UserViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="123456")

    def test_register(self):
        response = self.client.post("/register/", {"username":"newuser","password":"123456","email":"a@b.com"})
        self.assertEqual(response.status_code, 302)  # redirect sau đăng ký

    def test_login_logout(self):
        response = self.client.post("/login/", {"username":"testuser","password":"123456"})
        self.assertEqual(response.status_code, 302)
        response = self.client.get("/logout/")
        self.assertEqual(response.status_code, 302)
