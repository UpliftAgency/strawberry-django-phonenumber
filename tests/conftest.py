from unittest import mock

import pytest
import pytest_asyncio
from django.contrib.auth.hashers import make_password
from django.db import connections

from test_app.models import User


async def get_or_create_user(email, password, **kwargs):
    user, _ = await User.objects.aget_or_create(
        email=email,
        defaults=dict(password=make_password(password), **kwargs),
    )
    return user


@pytest_asyncio.fixture
async def user1():
    # Special case that doesn't trigger last_login error in async
    return await get_or_create_user(
        email="user1@example.com",
        password="password",
        phone_number="+1-415-418-3420",
        first_name="One",
        last_name="Phone",
    )


@pytest_asyncio.fixture
async def user2():
    # Special case that doesn't trigger last_login error in async
    return await get_or_create_user(
        email="user2@example.com",
        password="password",
    )


# This is a temporary fix
# See https://github.com/pytest-dev/pytest-asyncio/issues/226#issuecomment-1574929086
@pytest.fixture(autouse=True)
def fix_async_db():
    local = connections._connections
    ctx = local._get_context_id()
    for conn in connections.all():
        conn.inc_thread_sharing()
    conn = connections.all()[0]
    old = local._get_context_id
    try:
        with mock.patch.object(conn, "close"):
            object.__setattr__(local, "_get_context_id", lambda: ctx)
            yield
    finally:
        object.__setattr__(local, "_get_context_id", old)
