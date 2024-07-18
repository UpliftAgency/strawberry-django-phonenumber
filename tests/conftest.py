import contextlib
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
# See https://github.com/pytest-dev/pytest-asyncio/issues/226#issuecomment-2225156564
@pytest.fixture(autouse=True)
def fix_async_db(request):
    """
    If you don't use this fixture for async tests that use the ORM/database
    you won't get proper teardown of the database.
    This is a bug somehwere in pytest-django, pytest-asyncio or django itself.

    Nobody knows how to solve it, or who should solve it.
    Workaround here: https://github.com/django/channels/issues/1091#issuecomment-701361358
    More info:
    https://github.com/pytest-dev/pytest-django/issues/580
    https://code.djangoproject.com/ticket/32409
    https://github.com/pytest-dev/pytest-asyncio/issues/226


    The actual implementation of this workaround constists on ensuring
    Django always returns the same database connection independently of the thread
    the code that requests a db connection is in.

    We were unable to use better patching methods (the target is asgiref/local.py),
    so we resorted to mocking the _lock_storage context manager so that it returns a Mock.
    That mock contains the default connection of the main thread (instead of the connection
    of the running thread).

    This only works because our tests only ever use the default connection, which is the only
    thing our mock returns.

    We apologize in advance for the shitty implementation.
    """
    if (
        request.node.get_closest_marker("asyncio") is None
        or request.node.get_closest_marker("django_db") is None
    ):
        # Only run for async tests that use the database
        yield
        return

    main_thread_local = connections._connections
    for conn in connections.all():
        conn.inc_thread_sharing()

    main_thread_default_conn = main_thread_local._storage.default
    main_thread_storage = main_thread_local._lock_storage

    @contextlib.contextmanager
    def _lock_storage():
        yield mock.Mock(default=main_thread_default_conn)

    try:
        with mock.patch.object(main_thread_default_conn, "close"):
            object.__setattr__(main_thread_local, "_lock_storage", _lock_storage)
            yield
    finally:
        object.__setattr__(main_thread_local, "_lock_storage", main_thread_storage)
