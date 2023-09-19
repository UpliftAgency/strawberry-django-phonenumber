from typing import Optional

import strawberry
import strawberry_django
from asgiref.sync import sync_to_async
from strawberry.types import Info

from .types import User


@sync_to_async
def aget_user_from_request(request):
    return request.user if bool(request.user) else None


@strawberry.type
class Queries:
    @strawberry_django.field
    async def me(self, info: Info) -> Optional[User]:
        user = await aget_user_from_request(info.context.request)
        return user


schema = strawberry.Schema(query=Queries)
