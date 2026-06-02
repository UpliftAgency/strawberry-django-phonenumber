import json
from typing import Optional

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from strawberry.relay import to_base64

from .queries import GET_USER_WITH_PHONE_NUMBER

User = get_user_model()


@pytest.mark.django_db
class TestUsers:
    def send_and_get_data(
        self,
        client: Client,
        query: str,
        variables: dict | None = None,
        login_user: Optional[User] = None,
    ) -> dict:
        payload = {"query": query, "variables": variables}
        if login_user is not None:
            client.force_login(login_user)

        response = client.post(
            "/graphql/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        return response.json()

    def test_get_authenticated(self, client, user1, user2):
        response = self.send_and_get_data(
            client,
            query=GET_USER_WITH_PHONE_NUMBER,
            login_user=user1,
        )
        result = response["data"]
        assert "errors" not in result, result.get("errors")
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
