import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from firmy_django.models import Firma, SprawozdanieFinansowe


@pytest.mark.django_db
def test_invalid_xml_file_does_not_create_statement(client):
    user = User.objects.create_user(
        username="jan",
        password="Haslo123!"
    )

    firma = Firma.objects.create(
        owner=user,
        nazwa="ABC Sp. z o.o."
    )

    client.login(
        username="jan",
        password="Haslo123!"
    )

    xml_file = SimpleUploadedFile(
        "test.xml",
        b"to nie jest xml",
        content_type="text/xml"
    )

    client.post(
        reverse("importuj_xml", args=[firma.id]),
        {
            "plik_xml": xml_file
        }
    )

    assert SprawozdanieFinansowe.objects.count() == 0
