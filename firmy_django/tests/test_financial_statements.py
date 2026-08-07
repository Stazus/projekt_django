import pytest
from django.contrib.auth.models import User

from firmy_django.models import Firma, SprawozdanieFinansowe


@pytest.fixture
def firma(db):
    user = User.objects.create_user(
        username="jan",
        password="Haslo123!"
    )

    return Firma.objects.create(
        owner=user,
        nazwa="ABC Sp. z o.o.",
        nip="1234567890"
    )


@pytest.mark.django_db
def test_create_financial_statement(firma):
    sprawozdanie = SprawozdanieFinansowe.objects.create(
        firma=firma,
        rok=2024,
        naleznosci=1000
    )

    assert sprawozdanie.rok == 2024
    assert sprawozdanie.firma == firma


@pytest.mark.django_db
def test_archived_statement_is_marked(firma):
    sprawozdanie = SprawozdanieFinansowe.objects.create(
        firma=firma,
        rok=2024,
        czy_zarchiwizowane=True
    )

    assert sprawozdanie.czy_zarchiwizowane is True
