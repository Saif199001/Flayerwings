from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient


class AccountsAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_creates_session_and_profile(self):
        response = self.client.post(
            "/api/v1/auth/register/",
            {"username": "saif", "email": "saif@example.com", "password": "StrongPass123!", "password_confirm": "StrongPass123!", "display_name": "Saif"},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(username="saif")
        self.assertEqual(user.profile.display_name, "Saif")
        self.assertEqual(response.data["username"], "saif")

    def test_login_and_me(self):
        User.objects.create_user(username="saif", email="saif@example.com", password="StrongPass123!")
        response = self.client.post("/api/v1/auth/login/", {"username": "saif", "password": "StrongPass123!"}, format="json")
        self.assertEqual(response.status_code, 200)
        me = self.client.get("/api/v1/auth/me/")
        self.assertEqual(me.status_code, 200)
        self.assertEqual(me.data["username"], "saif")

    def test_invalid_login_rejected(self):
        User.objects.create_user(username="saif", password="StrongPass123!")
        response = self.client.post("/api/v1/auth/login/", {"username": "saif", "password": "wrong-password"}, format="json")
        self.assertEqual(response.status_code, 400)
