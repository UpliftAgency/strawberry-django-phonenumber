import asyncio
import json
from typing import Optional

import strawberry
from django.test import RequestFactory
from phonenumber_field.phonenumber import PhoneNumber as PhoneNumberField
from strawberry.django.views import GraphQLView

from strawberry_django_phonenumber import PhoneNumber

PHONE_NUMBER_QUERY = """
query {
  phoneNumber {
    asInternational
    asNational
    asE164
    asRfc3966
    countryCode
    nationalNumber
    extension
    rawInput
  }
}
"""

EXPECTED_PHONE_NUMBER = dict(
    asInternational="+1 415-418-3420",
    asNational="(415) 418-3420",
    asE164="+14154183420",
    asRfc3966="tel:+1-415-418-3420",
    countryCode="1",
    nationalNumber="4154183420",
    extension=None,
    rawInput="+14154183420",
)


@strawberry.type
class Query:
    @strawberry.field
    def phone_number(self) -> Optional[PhoneNumber]:
        return PhoneNumberField.from_string("+14154183420")


schema = strawberry.Schema(query=Query)


class TestPhoneNumberType:
    def test_execute_sync(self):
        result = schema.execute_sync(PHONE_NUMBER_QUERY)
        assert result.errors is None
        assert result.data == {"phoneNumber": EXPECTED_PHONE_NUMBER}

    def test_execute_async(self):
        result = asyncio.run(schema.execute(PHONE_NUMBER_QUERY))
        assert result.errors is None
        assert result.data == {"phoneNumber": EXPECTED_PHONE_NUMBER}

    def test_sync_django_view(self):
        request = RequestFactory().post(
            "/graphql/",
            data=json.dumps({"query": PHONE_NUMBER_QUERY}),
            content_type="application/json",
        )
        response = GraphQLView.as_view(schema=schema)(request)
        result = json.loads(response.content)
        assert "errors" not in result, result.get("errors")
        assert result["data"] == {"phoneNumber": EXPECTED_PHONE_NUMBER}
