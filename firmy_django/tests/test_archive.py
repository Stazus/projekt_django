import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from firmy_django.models import Firma, SprawozdanieFinansowe


@pytest.fixture
def archive_data(db):
    user = User.objects.create_user(
        username="jan",
        password="Haslo123!"
    )

    firma = Firma.objects.create(
        owner=user,
        nazwa="ABC Sp. z o.o."
    )

    sprawozdanie = SprawozdanieFinansowe.objects.create(
        firma=firma,
        rok=2024,
        naleznosci=1000
    )

    return user, firma, sprawozdanie


@pytest.mark.django_db
def test_archive_statement(client, archive_data):
    user, _, sprawozdanie = archive_data

    client.login(
        username="jan",
        password="Haslo123!"
    )

    client.get(
        reverse(
            "archiwizuj_sprawozdanie",
            args=[sprawozdanie.id]
        )
    )

    sprawozdanie.refresh_from_db()

    assert sprawozdanie.czy_zarchiwizowane is True


@pytest.mark.django_db
def test_restore_statement(client, archive_data):
    user, _, sprawozdanie = archive_data

    sprawozdanie.czy_zarchiwizowane = True
    sprawozdanie.save()

    client.login(
        username="jan",
        password="Haslo123!"
    )

    client.get(
        reverse(
            "przywroc_sprawozdanie",
            args=[sprawozdanie.id]
        )
    )

    sprawozdanie.refresh_from_db()

    assert sprawozdanie.czy_zarchiwizowane is False
