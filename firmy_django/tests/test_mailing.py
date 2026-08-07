import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from firmy_django.models import Mailing


@pytest.mark.django_db
def test_create_mailing():
    user = User.objects.create_user(
        username="jan",
        password="Haslo123!"
    )

    mailing = Mailing.objects.create(
        owner=user,
        temat="Test",
        tresc="Treść",
        odbiorcy_zewnetrzni="jan@example.com, adam@example.com"
    )

    assert mailing.temat == "Test"
    assert mailing.owner == user
    assert mailing.liczba_dodatkowych_odbiorcow == 2
    assert mailing.liczba_odbiorcow == 2


@pytest.mark.django_db
def test_user_sees_only_own_mailings(client):
    user1 = User.objects.create_user(
        username="jan",
        password="Haslo123!"
    )

    user2 = User.objects.create_user(
        username="adam",
        password="Haslo123!"
    )

    Mailing.objects.create(
        owner=user1,
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

    client.login(
        username="jan",
        password="Haslo123!"
    )

    response = client.get(
        reverse("historia_mailingow")
    )

    content = response.content.decode("utf-8")

    assert "Mój mailing" in content
    assert "Cudzy mailing" not in content
