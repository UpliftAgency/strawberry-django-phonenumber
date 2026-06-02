import pytest
from django.contrib.auth.hashers import make_password

from test_app.models import User


@pytest.fixture
def user1(db):
    user, _ = User.objects.get_or_create(
        email="user1@example.com",
        defaults=dict(
            password=make_password("password"),
            phone_number="+1-415-418-3420",
            first_name="One",
            last_name="Phone",
        ),
    )
    return user


@pytest.fixture
def user2(db):
    user, _ = User.objects.get_or_create(
        email="user2@example.com",
        defaults=dict(password=make_password("password")),
    )
    return user
