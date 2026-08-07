import pytest
from decimal import Decimal
from unittest.mock import mock_open, patch

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from firmy_django.models import Firma, SprawozdanieFinansowe


@pytest.fixture
def xml_data(db, client):
    user = User.objects.create_user(
        username="xml_user",
        password="Haslo123!"
    )

    firma = Firma.objects.create(
        owner=user,
        nazwa="ABC Sp. z o.o.",
        nip="1234567890",
        krs="0000123456"
    )

    client.login(
        username="xml_user",
        password="Haslo123!"
    )

    return user, firma, client


def przygotuj_xml(
    nazwa="ABC Sp. z o.o.",
    nip="1234567890",
    krs="0000123456",
    rok=2024,
    naleznosci="1250.50",
):
    zawartosc = f"""<?xml version="1.0" encoding="UTF-8"?>
<Sprawozdanie>
    <NazwaFirmy>{nazwa}</NazwaFirmy>
    <P_1D>{nip}</P_1D>
    <P_1E>{krs}</P_1E>
    <OkresDo>{rok}-12-31</OkresDo>
    <Aktywa_B_II>
        <KwotaA>{naleznosci}</KwotaA>
    </Aktywa_B_II>
</Sprawozdanie>
"""

    return SimpleUploadedFile(
        f"sprawozdanie_{rok}.xml",
        zawartosc.encode("utf-8"),
        content_type="text/xml"
    )


def importuj_do_wybranej_firmy(client, firma, xml_file):
    with (
        patch("firmy_django.views.os.makedirs"),
        patch("builtins.open", mock_open()),
    ):
        return client.post(
            reverse(
                "importuj_xml",
                args=[firma.id]
            ),
            {
                "plik_xml": xml_file
            }
        )


@pytest.mark.django_db
def test_valid_xml_creates_statement_for_existing_company(xml_data):
    _, firma, client = xml_data

    response = importuj_do_wybranej_firmy(
        client,
        firma,
        przygotuj_xml()
    )

    assert response.status_code == 200

    sprawozdanie = SprawozdanieFinansowe.objects.get(
        firma=firma,
        rok=2024
    )

    assert sprawozdanie.naleznosci == Decimal("1250.50")


@pytest.mark.django_db
def test_repeated_import_does_not_create_duplicate_statement(xml_data):
    _, firma, client = xml_data

    SprawozdanieFinansowe.objects.create(
        firma=firma,
        rok=2024,
        naleznosci=Decimal("800.00")
    )

    response = importuj_do_wybranej_firmy(
        client,
        firma,
        przygotuj_xml(
            naleznosci="900.00"
        )
    )

    assert response.status_code == 200

    assert SprawozdanieFinansowe.objects.filter(
        firma=firma,
        rok=2024
    ).count() == 1

    sprawozdanie = SprawozdanieFinansowe.objects.get(
        firma=firma,
        rok=2024
    )

    assert sprawozdanie.naleznosci == Decimal("800.00")


@pytest.mark.django_db
def test_import_updates_zero_receivables_from_xml(xml_data):
    _, firma, client = xml_data

    sprawozdanie = SprawozdanieFinansowe.objects.create(
        firma=firma,
        rok=2024,
        naleznosci=Decimal("0.00")
    )

    response = importuj_do_wybranej_firmy(
        client,
        firma,
        przygotuj_xml(
            naleznosci="1750.25"
        )
    )

    assert response.status_code == 200

    sprawozdanie.refresh_from_db()

    assert sprawozdanie.naleznosci == Decimal("1750.25")


@pytest.mark.django_db
def test_xml_for_unknown_company_creates_new_company_and_statement(xml_data):
    user, firma, client = xml_data

    response = importuj_do_wybranej_firmy(
        client,
        firma,
        przygotuj_xml(
            nazwa="Nowa Firma Sp. z o.o.",
            nip="9999999999",
            krs="0000999999",
            rok=2023,
            naleznosci="5000.00"
        )
    )

    assert response.status_code == 200

    nowa_firma = Firma.objects.get(
        owner=user,
        nip="9999999999"
    )

    assert nowa_firma.nazwa == "Nowa Firma Sp. z o.o."

    assert SprawozdanieFinansowe.objects.filter(
        firma=nowa_firma,
        rok=2023,
        naleznosci=Decimal("5000.00")
    ).exists()


@pytest.mark.django_db
def test_import_does_not_attach_statement_to_other_users_company(xml_data):
    user, firma, client = xml_data

    other_user = User.objects.create_user(
        username="other_xml_user",
        password="Haslo123!"
    )

    other_company = Firma.objects.create(
        owner=other_user,
        nazwa="Firma innego użytkownika",
        nip="7777777777",
        krs="0000777777"
    )

    response = importuj_do_wybranej_firmy(
        client,
        firma,
        przygotuj_xml(
            nazwa="Moja firma z XML",
            nip="7777777777",
            krs="0000777777",
            rok=2022,
            naleznosci="3000.00"
        )
    )

    assert response.status_code == 200

    assert not SprawozdanieFinansowe.objects.filter(
        firma=other_company
    ).exists()

    moja_firma = Firma.objects.get(
        owner=user,
        nip="7777777777"
    )

    assert SprawozdanieFinansowe.objects.filter(
        firma=moja_firma,
        rok=2022
    ).exists()
