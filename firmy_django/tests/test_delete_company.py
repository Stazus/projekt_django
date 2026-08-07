import pytest
from django.contrib.auth.models import User

from firmy_django.models import Firma, SprawozdanieFinansowe


@pytest.fixture
def firma_do_usuniecia(db):
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
def test_delete_company(firma_do_usuniecia):
    firma_do_usuniecia.delete()

    assert Firma.objects.count() == 0


@pytest.mark.django_db
def test_delete_company_removes_related_statements(firma_do_usuniecia):
    SprawozdanieFinansowe.objects.create(
        firma=firma_do_usuniecia,
        rok=2024,
        naleznosci=1000
    )

    firma_do_usuniecia.delete()

    assert Firma.objects.count() == 0
    assert SprawozdanieFinansowe.objects.count() == 0
