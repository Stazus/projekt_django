import pytest
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.mark.django_db
def test_user_can_log_in_with_correct_credentials(client):
    User.objects.create_user(
        username="jan",
        password="Haslo123!"
    )

    login_successful = client.login(
        username="jan",
        password="Haslo123!"
    )

    assert login_successful is True


@pytest.mark.django_db
def test_user_cannot_log_in_with_wrong_password(client):
    User.objects.create_user(
        username="jan",
        password="Haslo123!"
    )

    login_successful = client.login(
        username="jan",
        password="ZleHaslo123!"
    )

    assert login_successful is False


@pytest.mark.django_db
def test_registration_creates_new_user(client):
    response = client.post(
        reverse("rejestracja"),
        {
            "username": "adam",
            "email": "adam@example.com",
            "password1": "Haslo123!",
            "password2": "Haslo123!",
        }
    )

    assert response.status_code == 302
    assert User.objects.filter(username="adam").exists()
