import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from firmy_django.models import Firma


@pytest.mark.django_db
def test_filter_company_by_name(client):
    user = User.objects.create_user(
        username="jan",
        password="Haslo123!"
    )

    Firma.objects.create(
        owner=user,
        nazwa="Amazon",
        nip="1111111111"
    )

    Firma.objects.create(
        owner=user,
        nazwa="Google",
        nip="2222222222"
    )

    client.login(
        username="jan",
        password="Haslo123!"
    )

    response = client.get(
        reverse("home"),
        {"q": "Amazon"}
    )

    content = response.content.decode("utf-8")

    assert "Amazon" in content
    assert "Google" not in content
