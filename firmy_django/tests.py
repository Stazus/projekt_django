from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Firma, SprawozdanieFinansowe, Mailing, Branza, ProfilFirmy
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APIClient

from datetime import timedelta
from django.utils import timezone
from rest_framework_simplejwt.tokens import AccessToken

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
        

class DeleteCompanyTests(TestCase):

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

    def test_delete_company(self):
        self.firma.delete()

        self.assertEqual(Firma.objects.count(), 0)

    def test_delete_company_removes_related_statements(self):
        SprawozdanieFinansowe.objects.create(
            firma=self.firma,
            rok=2024,
            naleznosci=1000
        )

        self.firma.delete()

        self.assertEqual(Firma.objects.count(), 0)
        self.assertEqual(SprawozdanieFinansowe.objects.count(), 0)
        
        
class CompanyFilterTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="jan",
            password="Haslo123!"
        )

        Firma.objects.create(
            owner=self.user,
            nazwa="Amazon",
            nip="1111111111"
        )

        Firma.objects.create(
            owner=self.user,
            nazwa="Google",
            nip="2222222222"
        )

        self.client.login(
            username="jan",
            password="Haslo123!"
        )

    def test_filter_company_by_name(self):
        response = self.client.get(
            reverse("home"),
            {"q": "Amazon"}
        )

        self.assertContains(response, "Amazon")
        self.assertNotContains(response, "Google")
        

class XmlImportTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="jan",
            password="Haslo123!"
        )

        self.firma = Firma.objects.create(
            owner=self.user,
            nazwa="ABC Sp. z o.o."
        )

        self.client.login(
            username="jan",
            password="Haslo123!"
        )

    def test_invalid_xml_file_does_not_create_statement(self):
        xml_file = SimpleUploadedFile(
            "test.xml",
            b"to nie jest xml",
            content_type="text/xml"
        )

        response = self.client.post(
            reverse(
                "importuj_xml",
                args=[self.firma.id]
            ),
            {
                "plik_xml": xml_file
            }
        )

        self.assertContains(
            response,
            "nie jest poprawnym plikiem XML"
        )

        self.assertEqual(
            SprawozdanieFinansowe.objects.count(),
            0
        )
        
        
class ArchiveTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="jan",
            password="Haslo123!"
        )

        self.firma = Firma.objects.create(
            owner=self.user,
            nazwa="ABC Sp. z o.o."
        )

        self.sprawozdanie = SprawozdanieFinansowe.objects.create(
            firma=self.firma,
            rok=2024,
            naleznosci=1000
        )

        self.client.login(
            username="jan",
            password="Haslo123!"
        )

    def test_archive_statement(self):
        response = self.client.get(
            reverse(
                "archiwizuj_sprawozdanie",
                args=[self.sprawozdanie.id]
            )
        )

        self.sprawozdanie.refresh_from_db()

        self.assertTrue(
            self.sprawozdanie.czy_zarchiwizowane
        )

    def test_restore_statement(self):
        self.sprawozdanie.czy_zarchiwizowane = True
        self.sprawozdanie.save()

        response = self.client.get(
            reverse(
                "przywroc_sprawozdanie",
                args=[self.sprawozdanie.id]
            )
        )

        self.sprawozdanie.refresh_from_db()

        self.assertFalse(
            self.sprawozdanie.czy_zarchiwizowane
        )
        
        
class MailingTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="jan",
            password="Haslo123!"
        )

        self.client.login(
            username="jan",
            password="Haslo123!"
        )
        
        
    def test_create_mailing(self):
        mailing = Mailing.objects.create(
            owner=self.user,
            temat="Test",
            tresc="Treść",
            odbiorcy_zewnetrzni="jan@example.com, adam@example.com"
        )

        self.assertEqual(mailing.temat, "Test")
        self.assertEqual(mailing.owner, self.user)
        self.assertEqual(mailing.liczba_dodatkowych_odbiorcow, 2)
        self.assertEqual(mailing.liczba_odbiorcow, 2)
        

    def test_user_sees_only_own_mailings(self):
        user2 = User.objects.create_user(
            username="adam",
            password="Haslo123!"
        )
        
        Mailing.objects.create(
            owner=self.user,
            temat="Mój mailing",
            tresc="abc",
            odbiorcy_zewnetrzni="moj@example.com"
        )

        Mailing.objects.create(
            owner=user2,
            temat="Cudzy mailing",
            tresc="xyz",
            odbiorcy_zewnetrzni="cudzy@example.com"
        )
        
        response = self.client.get(
            reverse("historia_mailingow")
        )

        self.assertContains(response, "Mój mailing")
        self.assertNotContains(response, "Cudzy mailing")
        
        
class CompanyProfileAndIndustryTests(TestCase):

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

        self.client.login(
            username="jan",
            password="Haslo123!"
        )
        
    def test_company_can_have_profile(self):
        self.firma.telefon = "123456789"
        self.firma.strona_www = "https://firma.pl"
        self.firma.save()

        profil = ProfilFirmy.objects.create(
            firma=self.firma,
            opis="Firma transportowa"
        )

        self.assertEqual(profil.firma, self.firma)
        self.assertEqual(self.firma.profil, profil)
        self.assertEqual(profil.opis, "Firma transportowa")
        self.assertEqual(self.firma.telefon, "123456789")

    def test_company_can_have_many_industries(self):
        transport = Branza.objects.create(nazwa="Transport")
        logistyka = Branza.objects.create(nazwa="Logistyka")

        self.firma.branze.add(transport, logistyka)

        self.assertEqual(self.firma.branze.count(), 2)
        self.assertIn(transport, self.firma.branze.all())
        self.assertIn(logistyka, self.firma.branze.all())

    def test_company_detail_displays_profile_and_industries(self):
        transport = Branza.objects.create(nazwa="Transport")

        self.firma.branze.add(transport)
        self.firma.telefon = "123456789"
        self.firma.save()

        ProfilFirmy.objects.create(
            firma=self.firma,
            opis="Firma transportowa"
        )

        response = self.client.get(
            reverse("szczegoly_firmy", args=[self.firma.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Transport")
        self.assertContains(response, "Firma transportowa")
        self.assertContains(response, "123456789")
        
        
    def test_owner_can_create_company_profile(self):
        response = self.client.post(
            reverse(
                "edytuj_profil_firmy",
                args=[self.firma.id]
            ),
            {
                "opis": "Nowy opis działalności firmy",
            }
        )

        self.assertRedirects(
            response,
            reverse(
                "szczegoly_firmy",
                args=[self.firma.id]
            )
        )

        profil = ProfilFirmy.objects.get(firma=self.firma)

        self.assertEqual(
            profil.opis,
            "Nowy opis działalności firmy"
        )

    def test_owner_can_update_existing_company_profile(self):
        profil = ProfilFirmy.objects.create(
            firma=self.firma,
            opis="Stary opis"
        )

        response = self.client.post(
            reverse(
                "edytuj_profil_firmy",
                args=[self.firma.id]
            ),
            {
                "opis": "Zaktualizowany opis",
            }
        )

        self.assertRedirects(
            response,
            reverse(
                "szczegoly_firmy",
                args=[self.firma.id]
            )
        )

        profil.refresh_from_db()

        self.assertEqual(
            profil.opis,
            "Zaktualizowany opis"
        )

        self.assertEqual(
            ProfilFirmy.objects.filter(
                firma=self.firma
            ).count(),
            1
        )

    def test_user_cannot_edit_another_users_company_profile(self):
        other_user = User.objects.create_user(
            username="anna",
            password="Haslo456!"
        )

        other_company = Firma.objects.create(
            owner=other_user,
            nazwa="Firma innego użytkownika",
            nip="9876543210"
        )

        response = self.client.get(
            reverse(
                "edytuj_profil_firmy",
                args=[other_company.id]
            )
        )

        self.assertEqual(response.status_code, 404)

        self.assertFalse(
            ProfilFirmy.objects.filter(
                firma=other_company
            ).exists()
        )
        
    def test_logo_txt_file_is_rejected(self):
        from django.core.files.uploadedfile import SimpleUploadedFile

        txt = SimpleUploadedFile(
            "logo.txt",
            b"To nie jest obraz",
            content_type="text/plain"
        )

        response = self.client.post(
            reverse("edytuj_profil_firmy", args=[self.firma.id]),
            {
                "opis": "Opis",
                "logo": txt,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Logo musi być plikiem JPG, PNG lub WebP."
        )
        
    def test_banner_txt_file_is_rejected(self):
        from django.core.files.uploadedfile import SimpleUploadedFile

        txt = SimpleUploadedFile(
            "banner.txt",
            b"To nie jest obraz",
            content_type="text/plain"
        )

        response = self.client.post(
            reverse("edytuj_profil_firmy", args=[self.firma.id]),
            {
                "opis": "Opis",
                "banner": txt,
            },
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response,
            "Banner musi być plikiem JPG, PNG lub WebP."
        )
        
    def test_existing_logo_is_preserved_when_only_description_is_updated(self):
        logo = SimpleUploadedFile(
            "logo.png",
            b"fake-image-content",
            content_type="image/png",
        )

        profil = ProfilFirmy.objects.create(
            firma=self.firma,
            opis="Stary opis",
            logo=logo,
        )

        old_logo_name = profil.logo.name

        response = self.client.post(
            reverse("edytuj_profil_firmy", args=[self.firma.id]),
            {
                "opis": "Nowy opis",
            },
        )

        self.assertRedirects(
            response,
            reverse("szczegoly_firmy", args=[self.firma.id]),
        )

        profil.refresh_from_db()

        self.assertEqual(profil.opis, "Nowy opis")
        self.assertEqual(profil.logo.name, old_logo_name)
        
    def test_too_large_logo_is_rejected(self):
        large_logo = SimpleUploadedFile(
            "logo.png",
            b"x" * (2 * 1024 * 1024 + 1),
            content_type="image/png",
        )

        response = self.client.post(
            reverse("edytuj_profil_firmy", args=[self.firma.id]),
            {
                "opis": "Opis",
                "logo": large_logo,
            },
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response,
            "Logo nie może być większe niż 2 MB."
        )

        profil = ProfilFirmy.objects.get(firma=self.firma)

        self.assertEqual(profil.logo.name, "")
        
class RestApiTests(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1",
            password="Haslo123!"
        )
        self.user2 = User.objects.create_user(
            username="user2",
            password="Haslo123!"
        )

        self.firma_user1 = Firma.objects.create(
            owner=self.user1,
            nazwa="ASAJ Sp. z o.o.",
            nip="1111111111"
        )

        self.firma_user2 = Firma.objects.create(
            owner=self.user2,
            nazwa="Cudza firma",
            nip="2222222222"
        )

        self.branza = Branza.objects.create(
            nazwa="Transport"
        )
        self.firma_user1.branze.add(self.branza)
        self.firma_user1.telefon = "123456789"
        self.firma_user1.save()

        ProfilFirmy.objects.create(
            firma=self.firma_user1,
            opis="Firma transportowa"
        )

        self.sprawozdanie = SprawozdanieFinansowe.objects.create(
            firma=self.firma_user1,
            rok=2024,
            naleznosci=1000
        )

        self.client = APIClient()
        
    def test_api_requires_authentication(self):
        response = self.client.get("/api/firmy/")

        self.assertEqual(response.status_code, 401)

    def test_user_sees_only_own_companies_in_api(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.get("/api/firmy/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ASAJ Sp. z o.o.")
        self.assertNotContains(response, "Cudza firma")

    def test_user_cannot_access_other_user_company_in_api(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.get(
            f"/api/firmy/{self.firma_user2.id}/"
        )

        self.assertEqual(response.status_code, 404)

    def test_company_detail_api_displays_profile_and_industries(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.get(
            f"/api/firmy/{self.firma_user1.id}/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Transport")
        self.assertContains(response, "Firma transportowa")
        self.assertContains(response, "123456789")

    def test_api_company_search(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.get(
            "/api/firmy/?search=ASAJ"
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ASAJ Sp. z o.o.")

    def test_api_financial_statement_list(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.get(
            "/api/sprawozdania/?search=2024"
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "2024")
        self.assertContains(response, "1000.00")
                

    def test_jwt_token_obtain(self):
        response = self.client.post(
            "/api/token/",
            {
                "username": "user1",
                "password": "Haslo123!"
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)   


    def test_jwt_token_refresh(self):
        token_response = self.client.post(
            "/api/token/",
            {
                "username": "user1",
                "password": "Haslo123!"
            },
            format="json",
        )

        refresh_token = token_response.data["refresh"]

        response = self.client.post(
            "/api/token/refresh/",
            {
                "refresh": refresh_token
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)


    def test_jwt_access_token_allows_api_access(self):
        token_response = self.client.post(
            "/api/token/",
            {
                "username": "user1",
                "password": "Haslo123!"
            },
            format="json",
        )

        access_token = token_response.data["access"]

        response = self.client.get(
            "/api/firmy/",
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ASAJ Sp. z o.o.")
        self.assertNotContains(response, "Cudza firma")
        
        
    def test_jwt_wrong_password_returns_401(self):
        response = self.client.post(
            "/api/token/",
            {
                "username": "user1",
                "password": "ZleHaslo123!"
            },
            format="json",
        )

        self.assertEqual(response.status_code, 401)
        
        
    def test_expired_jwt_token_returns_401(self):
        token = AccessToken.for_user(self.user1)

        token.set_exp(
            from_time=timezone.now() - timedelta(minutes=10),
            lifetime=timedelta(minutes=1),
        )

        response = self.client.get(
            "/api/firmy/",
            HTTP_AUTHORIZATION=f"Bearer {str(token)}"
        )

        self.assertEqual(response.status_code, 401)
        
        
