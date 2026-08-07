import pytest
from datetime import timedelta

from django.contrib.auth.models import User
from django.utils import timezone

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from firmy_django.models import (
    Firma,
    Branza,
    ProfilFirmy,
    SprawozdanieFinansowe,
)


@pytest.fixture
def api_data(db):
    user1 = User.objects.create_user(
        username="user1",
        password="Haslo123!"
    )

    user2 = User.objects.create_user(
        username="user2",
        password="Haslo123!"
    )

    firma_user1 = Firma.objects.create(
        owner=user1,
        nazwa="ASAJ Sp. z o.o.",
        nip="1111111111"
    )

    firma_user2 = Firma.objects.create(
        owner=user2,
        nazwa="Cudza firma",
        nip="2222222222"
    )

    branza = Branza.objects.create(
        nazwa="Transport"
    )

    firma_user1.branze.add(branza)
    firma_user1.telefon = "123456789"
    firma_user1.save()

    ProfilFirmy.objects.create(
        firma=firma_user1,
        opis="Firma transportowa"
    )

    sprawozdanie = SprawozdanieFinansowe.objects.create(
        firma=firma_user1,
        rok=2024,
        naleznosci=1000
    )

    client = APIClient()

    return {
        "user1": user1,
        "user2": user2,
        "firma_user1": firma_user1,
        "firma_user2": firma_user2,
        "sprawozdanie": sprawozdanie,
        "client": client,
    }


@pytest.mark.django_db
def test_api_requires_authentication(api_data):
    response = api_data["client"].get("/api/firmy/")

    assert response.status_code == 401


@pytest.mark.django_db
def test_user_sees_only_own_companies_in_api(api_data):
    client = api_data["client"]
    client.force_authenticate(user=api_data["user1"])

    response = client.get("/api/firmy/")

    content = response.content.decode("utf-8")

    assert response.status_code == 200
    assert "ASAJ Sp. z o.o." in content
    assert "Cudza firma" not in content


@pytest.mark.django_db
def test_user_cannot_access_other_user_company_in_api(api_data):
    client = api_data["client"]
    client.force_authenticate(user=api_data["user1"])

    response = client.get(
        f'/api/firmy/{api_data["firma_user2"].id}/'
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_company_detail_api_displays_profile_and_industries(api_data):
    client = api_data["client"]
    client.force_authenticate(user=api_data["user1"])

    response = client.get(
        f'/api/firmy/{api_data["firma_user1"].id}/'
    )

    content = response.content.decode("utf-8")

    assert response.status_code == 200
    assert "Transport" in content
    assert "Firma transportowa" in content
    assert "123456789" in content


@pytest.mark.django_db
def test_api_company_search(api_data):
    client = api_data["client"]
    client.force_authenticate(user=api_data["user1"])

    response = client.get(
        "/api/firmy/?search=ASAJ"
    )

    content = response.content.decode("utf-8")

    assert response.status_code == 200
    assert "ASAJ Sp. z o.o." in content


@pytest.mark.django_db
def test_api_financial_statement_list(api_data):
    client = api_data["client"]
    client.force_authenticate(user=api_data["user1"])

    response = client.get(
        "/api/sprawozdania/?search=2024"
    )

    content = response.content.decode("utf-8")

    assert response.status_code == 200
    assert "2024" in content
    assert "1000.00" in content


@pytest.mark.django_db
def test_jwt_token_obtain(api_data):
    response = api_data["client"].post(
        "/api/token/",
        {
            "username": "user1",
            "password": "Haslo123!"
        },
        format="json",
    )

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_jwt_token_refresh(api_data):
    client = api_data["client"]

    token_response = client.post(
        "/api/token/",
        {
            "username": "user1",
            "password": "Haslo123!"
        },
        format="json",
    )

    refresh_token = token_response.data["refresh"]

    response = client.post(
        "/api/token/refresh/",
        {
            "refresh": refresh_token
        },
        format="json",
    )

    assert response.status_code == 200
    assert "access" in response.data


@pytest.mark.django_db
def test_jwt_access_token_allows_api_access(api_data):
    client = api_data["client"]

    token_response = client.post(
        "/api/token/",
        {
            "username": "user1",
            "password": "Haslo123!"
        },
        format="json",
    )

    access_token = token_response.data["access"]

    response = client.get(
        "/api/firmy/",
        HTTP_AUTHORIZATION=f"Bearer {access_token}"
    )

    content = response.content.decode("utf-8")

    assert response.status_code == 200
    assert "ASAJ Sp. z o.o." in content
    assert "Cudza firma" not in content


@pytest.mark.django_db
def test_jwt_wrong_password_returns_401(api_data):
    response = api_data["client"].post(
        "/api/token/",
        {
            "username": "user1",
            "password": "ZleHaslo123!"
        },
        format="json",
    )

    assert response.status_code == 401


@pytest.mark.django_db
def test_expired_jwt_token_returns_401(api_data):
    token = AccessToken.for_user(api_data["user1"])

    token.set_exp(
        from_time=timezone.now() - timedelta(minutes=10),
        lifetime=timedelta(minutes=1),
    )

    response = api_data["client"].get(
        "/api/firmy/",
        HTTP_AUTHORIZATION=f"Bearer {str(token)}"
    )

    assert response.status_code == 401
