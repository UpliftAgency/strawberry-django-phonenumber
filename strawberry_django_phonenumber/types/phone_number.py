"""Phone number GraphQL type."""

from typing import Optional

import strawberry
from phonenumber_field.phonenumber import PhoneNumber as PhoneNumberField
from strawberry.types import Info


@strawberry.type
class PhoneNumber:
    """GraphQL type for the phone number."""

    @strawberry.field
    def as_international(root: PhoneNumberField, info: Info) -> str:
        return root.as_international

    @strawberry.field
    def as_national(root: PhoneNumberField, info: Info) -> str:
        return root.as_national

    @strawberry.field
    def as_e164(root: PhoneNumberField, info: Info) -> str:
        return root.as_e164

    @strawberry.field
    def as_rfc3966(root: PhoneNumberField, info: Info) -> str:
        return root.as_rfc3966

    @strawberry.field
    def country_code(root: PhoneNumberField, info: Info) -> str:
        return root.country_code

    @strawberry.field
    def national_number(root: PhoneNumberField, info: Info) -> str:
        return root.national_number

    @strawberry.field
    def extension(root: PhoneNumberField, info: Info) -> Optional[str]:
        return root.extension

    @strawberry.field
    def raw_input(root: PhoneNumberField, info: Info) -> str:
        return root.raw_input
