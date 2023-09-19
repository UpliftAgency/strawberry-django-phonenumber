from typing import Optional

import pytest
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from django.test import Client
from strawberry.relay import to_base64

from .queries import GET_USER_WITH_PHONE_NUMBER

User = get_user_model()


@pytest.mark.asyncio
@pytest.mark.django_db
class TestUsers:
    async def login(self, user, async_client: Client):
        await sync_to_async(async_client.force_login)(user)

    async def send_and_get_data(
        self,
        async_client: Client,
        query: str,
        variables: dict = None,
        login_user: Optional[User] = None,
        request_kwargs: Optional[dict] = None,
    ) -> dict:
        payload = dict(query=query, variables=variables)
        request_kwargs = request_kwargs or dict()
        if login_user:
            await self.login(login_user, async_client)

            response = await async_client.post(
                "/graphql/", payload, content_type="application/json", **request_kwargs
            )

        response = response.json()

        return response

    async def test_get_authenticated(self, async_client, user1, user2):
        response = await self.send_and_get_data(
            async_client,
            query=GET_USER_WITH_PHONE_NUMBER,
            login_user=user1,
        )
        result = response["data"]
        assert "errors" not in result, result["errors"]
        assert "me" in result

        assert dict(result["me"]) == dict(
            id=to_base64(User.__name__, user1.id),
            firstName=user1.first_name,
            lastName=user1.last_name,
            phoneNumber=dict(
                asInternational="+1 415-418-3420",
                asE164="+14154183420",
                asNational="(415) 418-3420",
                asRfc3966="tel:+1-415-418-3420",
                countryCode="1",
                extension=None,
                nationalNumber="4154183420",
                rawInput="+14154183420",
            ),
        )
