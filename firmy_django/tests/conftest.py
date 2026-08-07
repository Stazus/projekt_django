import pytest
from django.contrib.auth.models import User


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="testuser",
        password="Test123!"
    )


@pytest.fixture
def client_logged(client, user):
    client.login(
        username="testuser",
        password="Test123!"
    )
    return client
