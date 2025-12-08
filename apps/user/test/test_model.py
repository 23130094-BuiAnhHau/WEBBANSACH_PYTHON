from django.test import TestCase
from apps.user.models import User


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="hau",
            password="123456",
            email="hau@example.com"
        )

    def test_user_to_string(self):
        print("\n--- User __str__ ---")
        print(str(self.user))
        self.assertEqual(str(self.user), "hau")

    def test_user_fields(self):
        print("\n--- User fields ---")
        print("Username:", self.user.username)
        print("Email:", self.user.email)

        self.assertEqual(self.user.email, "hau@example.com")
        self.assertTrue(self.user.check_password("123456"))
