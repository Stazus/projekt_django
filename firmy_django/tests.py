from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthenticationTests(TestCase):
    def test_user_can_log_in_with_correct_credentials(self):
        User.objects.create_user(
            username="jan",
            password="Haslo123!"
        )

        login_successful = self.client.login(
            username="jan",
            password="Haslo123!"
        )

        self.assertTrue(login_successful)

    def test_user_cannot_log_in_with_wrong_password(self):
        User.objects.create_user(
            username="jan",
            password="Haslo123!"
        )

        login_successful = self.client.login(
            username="jan",
            password="ZleHaslo123!"
        )

        self.assertFalse(login_successful)
       
        
    def test_registration_creates_new_user(self):
        response = self.client.post(
            reverse("rejestracja"),
            {
                "username": "adam",
                "email": "adam@example.com",
                "password1": "Haslo123!",
                "password2": "Haslo123!",
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="adam").exists())