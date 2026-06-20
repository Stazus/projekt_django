from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Firma, SprawozdanieFinansowe


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
        
        
class FirmaOwnershipTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1",
            password="Haslo123!"
        )
        self.user2 = User.objects.create_user(
            username="user2",
            password="Haslo123!"
        )

    def test_user_can_create_own_company(self):
        firma = Firma.objects.create(
            owner=self.user1,
            nazwa="ABC Sp. z o.o.",
            nip="1234567890",
            miasto="Warszawa"
        )

        self.assertEqual(firma.owner, self.user1)
        self.assertEqual(Firma.objects.count(), 1)

    def test_user_sees_only_own_companies_on_list(self):
        Firma.objects.create(
            owner=self.user1,
            nazwa="Firma użytkownika 1",
            nip="1111111111"
        )
        Firma.objects.create(
            owner=self.user2,
            nazwa="Firma użytkownika 2",
            nip="2222222222"
        )

        self.client.login(
            username="user1",
            password="Haslo123!"
        )

        response = self.client.get(reverse("home"))

        self.assertContains(response, "Firma użytkownika 1")
        self.assertNotContains(response, "Firma użytkownika 2")

    def test_user_cannot_access_other_user_company_details(self):
        firma_user2 = Firma.objects.create(
            owner=self.user2,
            nazwa="Cudza firma",
            nip="2222222222"
        )

        self.client.login(
            username="user1",
            password="Haslo123!"
        )

        response = self.client.get(
            reverse("szczegoly_firmy", args=[firma_user2.id])
        )

        self.assertEqual(response.status_code, 404)
        
        
class SprawozdanieTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="jan",
            password="Haslo123!"
        )

        self.firma = Firma.objects.create(
            owner=self.user,
            nazwa="ABC Sp. z o.o.",
            nip="1234567890"
        )

    def test_create_financial_statement(self):
        sprawozdanie = SprawozdanieFinansowe.objects.create(
            firma=self.firma,
            rok=2024,
            naleznosci=1000
        )

        self.assertEqual(sprawozdanie.rok, 2024)
        self.assertEqual(sprawozdanie.firma, self.firma)

    def test_archived_statement_is_marked(self):
        sprawozdanie = SprawozdanieFinansowe.objects.create(
            firma=self.firma,
            rok=2024,
            czy_zarchiwizowane=True
        )

        self.assertTrue(sprawozdanie.czy_zarchiwizowane)
        


        
        
        