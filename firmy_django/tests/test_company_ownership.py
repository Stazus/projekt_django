import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from firmy_django.models import Firma


@pytest.fixture
def users(db):
    user1 = User.objects.create_user(
        username="user1",
        password="Haslo123!"
    )
    user2 = User.objects.create_user(
        username="user2",
        password="Haslo123!"
    )
    return user1, user2


@pytest.mark.django_db
def test_user_can_create_own_company(users):
    user1, _ = users

    firma = Firma.objects.create(
        owner=user1,
        nazwa="ABC Sp. z o.o.",
        nip="1234567890",
        miasto="Warszawa"
    )

    assert firma.owner == user1
    assert Firma.objects.count() == 1


@pytest.mark.django_db
def test_user_sees_only_own_companies_on_list(client, users):
    user1, user2 = users

    Firma.objects.create(
        owner=user1,
        nazwa="Firma użytkownika 1",
        nip="1111111111"
    )

    Firma.objects.create(
        owner=user2,
        nazwa="Firma użytkownika 2",
        nip="2222222222"
    )

    client.login(
        username="user1",
        password="Haslo123!"
    )

    response = client.get(reverse("home"))

    content = response.content.decode("utf-8")

    assert "Firma użytkownika 1" in content
    assert "Firma użytkownika 2" not in content


@pytest.mark.django_db
def test_user_cannot_access_other_user_company_details(client, users):
    user1, user2 = users

    firma_user2 = Firma.objects.create(
        owner=user2,
        nazwa="Cudza firma",
        nip="2222222222"
    )

    client.login(
        username="user1",
        password="Haslo123!"
    )

    response = client.get(
        reverse("szczegoly_firmy", args=[firma_user2.id])
    )

    assert response.status_code == 404
