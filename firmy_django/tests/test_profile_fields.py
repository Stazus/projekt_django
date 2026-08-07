import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from firmy_django.models import Firma, ProfilFirmy


@pytest.fixture
def profile_data(db, client):
    user = User.objects.create_user(
        username="profil_user",
        password="Haslo123!"
    )

    firma = Firma.objects.create(
        owner=user,
        nazwa="Firma Profilowa Sp. z o.o.",
        nip="1234567890"
    )

    client.login(
        username="profil_user",
        password="Haslo123!"
    )

    return user, firma, client


@pytest.mark.django_db
def test_profile_saves_phone_number(profile_data):
    _, firma, client = profile_data

    response = client.post(
        reverse(
            "edytuj_profil_firmy",
            args=[firma.id]
        ),
        {
            "opis": "Opis testowy firmy",
            "telefon": "+48 600 700 800",
            "strona_www": "",
        }
    )

    assert response.status_code == 302

    profil = ProfilFirmy.objects.get(firma=firma)

    assert profil.telefon == "+48 600 700 800"


@pytest.mark.django_db
def test_profile_saves_website(profile_data):
    _, firma, client = profile_data

    response = client.post(
        reverse(
            "edytuj_profil_firmy",
            args=[firma.id]
        ),
        {
            "opis": "Opis testowy firmy",
            "telefon": "",
            "strona_www": "https://example.pl",
        }
    )

    assert response.status_code == 302

    profil = ProfilFirmy.objects.get(firma=firma)

    assert profil.strona_www == "https://example.pl"


@pytest.mark.django_db
def test_company_details_display_phone_and_website(profile_data):
    _, firma, client = profile_data

    ProfilFirmy.objects.create(
        firma=firma,
        opis="Opis testowy firmy",
        telefon="+48 600 700 800",
        strona_www="https://example.pl"
    )

    response = client.get(
        reverse(
            "szczegoly_firmy",
            args=[firma.id]
        )
    )

    content = response.content.decode("utf-8")

    assert response.status_code == 200
    assert "+48 600 700 800" in content
    assert "https://example.pl" in content
