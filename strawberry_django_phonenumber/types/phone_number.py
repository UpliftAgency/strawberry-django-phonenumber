"""Phone number GraphQL type."""

from typing import Optional

import strawberry
from phonenumber_field.phonenumber import PhoneNumber as PhoneNumberField
from strawberry.types import Info


@strawberry.type
class PhoneNumber:
    """GraphQL type for the phone number."""

    @strawberry.field
    async def as_international(root: PhoneNumberField, info: Info) -> str:
        return root.as_international

    @strawberry.field
    async def as_national(root: PhoneNumberField, info: Info) -> str:
        return root.as_national

    @strawberry.field
    async def as_e164(root: PhoneNumberField, info: Info) -> str:
        return root.as_e164

    @strawberry.field
    async def as_rfc3966(root: PhoneNumberField, info: Info) -> str:
        return root.as_rfc3966

    @strawberry.field
    async def country_code(root: PhoneNumberField, info: Info) -> str:
        return root.country_code

    @strawberry.field
    async def national_number(root: PhoneNumberField, info: Info) -> str:
        return root.national_number

    @strawberry.field
    async def extension(root: PhoneNumberField, info: Info) -> Optional[str]:
        return root.extension

    @strawberry.field
    async def raw_input(root: PhoneNumberField, info: Info) -> str:
        return root.raw_input
