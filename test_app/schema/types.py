from typing import Optional, cast

import strawberry
import strawberry_django
from strawberry.types import Info

from strawberry_django_phonenumber import PhoneNumber

from .. import models


@strawberry_django.type(models.User, fields=["first_name", "last_name"])
class User(strawberry.relay.Node):
    """GraphQL type for the User model."""

    @strawberry_django.field
    async def phone_number(root, info: Info) -> Optional[PhoneNumber]:
        if not root.phone_number:
            return None
        return cast(PhoneNumber, root.phone_number)
