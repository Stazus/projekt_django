import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from firmy_django.models import Firma, Branza, ProfilFirmy


@pytest.fixture
def company_profile_data(db, client):
    user = User.objects.create_user(
        username="jan",
        password="Haslo123!"
    )

    firma = Firma.objects.create(
        owner=user,
        nazwa="ABC Sp. z o.o.",
        nip="1234567890"
    )

    client.login(
        username="jan",
        password="Haslo123!"
    )

    return user, firma, client


@pytest.mark.django_db
def test_company_can_have_profile(company_profile_data):
    _, firma, _ = company_profile_data

    firma.telefon = "123456789"
    firma.strona_www = "https://firma.pl"
    firma.save()

    profil = ProfilFirmy.objects.create(
        firma=firma,
        opis="Firma transportowa"
    )

    assert profil.firma == firma
    assert firma.profil == profil
    assert profil.opis == "Firma transportowa"
    assert firma.telefon == "123456789"


@pytest.mark.django_db
def test_company_can_have_many_industries(company_profile_data):
    _, firma, _ = company_profile_data

    transport = Branza.objects.create(nazwa="Transport")
    logistyka = Branza.objects.create(nazwa="Logistyka")

    firma.branze.add(transport, logistyka)

    assert firma.branze.count() == 2
    assert transport in firma.branze.all()
    assert logistyka in firma.branze.all()


@pytest.mark.django_db
def test_company_detail_displays_profile_and_industries(company_profile_data):
    _, firma, client = company_profile_data

    transport = Branza.objects.create(nazwa="Transport")
    firma.branze.add(transport)

    firma.telefon = "123456789"
    firma.save()

    ProfilFirmy.objects.create(
        firma=firma,
        opis="Firma transportowa"
    )

    response = client.get(
        reverse("szczegoly_firmy", args=[firma.id])
    )

    content = response.content.decode("utf-8")

    assert response.status_code == 200
    assert "Transport" in content
    assert "Firma transportowa" in content
    assert "123456789" in content


@pytest.mark.django_db
def test_owner_can_create_company_profile(company_profile_data):
    _, firma, client = company_profile_data

    response = client.post(
        reverse(
            "edytuj_profil_firmy",
            args=[firma.id]
        ),
        {
            "opis": "Nowy opis działalności firmy",
        }
    )

    assert response.status_code == 302
    assert response.url == reverse(
        "szczegoly_firmy",
        args=[firma.id]
    )

    profil = ProfilFirmy.objects.get(firma=firma)

    assert profil.opis == "Nowy opis działalności firmy"


@pytest.mark.django_db
def test_owner_can_update_existing_company_profile(company_profile_data):
    _, firma, client = company_profile_data

    profil = ProfilFirmy.objects.create(
        firma=firma,
        opis="Stary opis"
    )

    response = client.post(
        reverse(
            "edytuj_profil_firmy",
            args=[firma.id]
        ),
        {
            "opis": "Zaktualizowany opis",
        }
    )

    assert response.status_code == 302
    assert response.url == reverse(
        "szczegoly_firmy",
        args=[firma.id]
    )

    profil.refresh_from_db()

    assert profil.opis == "Zaktualizowany opis"
    assert ProfilFirmy.objects.filter(firma=firma).count() == 1


@pytest.mark.django_db
def test_user_cannot_edit_another_users_company_profile(company_profile_data):
    _, _, client = company_profile_data

    other_user = User.objects.create_user(
        username="anna",
        password="Haslo456!"
    )

    other_company = Firma.objects.create(
        owner=other_user,
        nazwa="Firma innego użytkownika",
        nip="9876543210"
    )

    response = client.get(
        reverse(
            "edytuj_profil_firmy",
            args=[other_company.id]
        )
    )

    assert response.status_code == 404
    assert not ProfilFirmy.objects.filter(
        firma=other_company
    ).exists()


@pytest.mark.django_db
def test_logo_txt_file_is_rejected(company_profile_data):
    _, firma, client = company_profile_data

    txt = SimpleUploadedFile(
        "logo.txt",
        b"To nie jest obraz",
        content_type="text/plain"
    )

    response = client.post(
        reverse("edytuj_profil_firmy", args=[firma.id]),
        {
            "opis": "Opis",
            "logo": txt,
        },
    )

    content = response.content.decode("utf-8")

    assert response.status_code == 200
    assert "Logo musi być plikiem JPG, PNG lub WebP." in content


@pytest.mark.django_db
def test_banner_txt_file_is_rejected(company_profile_data):
    _, firma, client = company_profile_data

    txt = SimpleUploadedFile(
        "banner.txt",
        b"To nie jest obraz",
        content_type="text/plain"
    )

    response = client.post(
        reverse("edytuj_profil_firmy", args=[firma.id]),
        {
            "opis": "Opis",
            "banner": txt,
        },
    )

    content = response.content.decode("utf-8")

    assert response.status_code == 200
    assert "Banner musi być plikiem JPG, PNG lub WebP." in content


@pytest.mark.django_db
def test_existing_logo_is_preserved_when_only_description_is_updated(
    company_profile_data
):
    _, firma, client = company_profile_data

    logo = SimpleUploadedFile(
        "logo.png",
        b"fake-image-content",
        content_type="image/png",
    )

    profil = ProfilFirmy.objects.create(
        firma=firma,
        opis="Stary opis",
        logo=logo,
    )

    old_logo_name = profil.logo.name

    response = client.post(
        reverse("edytuj_profil_firmy", args=[firma.id]),
        {
            "opis": "Nowy opis",
        },
    )

    assert response.status_code == 302
    assert response.url == reverse(
        "szczegoly_firmy",
        args=[firma.id]
    )

    profil.refresh_from_db()

    assert profil.opis == "Nowy opis"
    assert profil.logo.name == old_logo_name


@pytest.mark.django_db
def test_too_large_logo_is_rejected(company_profile_data):
    _, firma, client = company_profile_data

    large_logo = SimpleUploadedFile(
        "logo.png",
        b"x" * (2 * 1024 * 1024 + 1),
        content_type="image/png",
    )

    response = client.post(
        reverse("edytuj_profil_firmy", args=[firma.id]),
        {
            "opis": "Opis",
            "logo": large_logo,
        },
    )

    content = response.content.decode("utf-8")

    assert response.status_code == 200
    assert "Logo nie może być większe niż 2 MB." in content

    profil = ProfilFirmy.objects.get(firma=firma)

    assert profil.logo.name == ""
