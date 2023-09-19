# strawberry-django-phonenumber

![build status](https://github.com/UpliftAgency/strawberry-django-phonenumber/actions/workflows/pythonpackage.yml/badge.svg)

## Introduction

GraphQL types for Phone Numbers with Strawberry Django. If you use `django`, `strawberry`, and `django-phonenumber-field`, this library is for you.

Supported on:

* Python 3.9+ (likely earlier versions too, needs tested)
* Django 3+
* strawberry-graphql-django 0.17+
* django-phonenumber-field 7+

Here's how it works. Automagically get this query:

```graphql
query User {
  phoneNumber {
    ...phoneNumberFragment
  }
}

fragment phoneNumberFragment on PhoneNumber {
    asInternational  # +1 415-418-3420
    asNational  # (415) 418-3420
    asE164
    asRfc3966
    countryCode  # 1
    nationalNumber
    extension
    rawInput
}
```

With this code:

```python
# yourapp/models.py
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    phone_number = PhoneNumberField(blank=True)

# yourapp/graphql/types.py
from typing import Optional, cast

import strawberry
import strawberry_django
from strawberry.types import Info
from strawberry_django_phonenumber import PhoneNumber

from yourapp import models



@strawberry_django.type(models.User)
class User(strawberry.relay.Node):
    """GraphQL type for the User model."""

    @strawberry_django.field
    async def phone_number(root, info: Info) -> Optional[PhoneNumber]:
        if not root.phone_number:
            return None
        return cast(PhoneNumber, root.phone_number)

# yourapp/graphql/__init__.py
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

# yourapp/urls.py

from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from strawberry.django.views import AsyncGraphQLView

from .graphql import schema

urlpatterns = [
    path(
        "graphql/",
        csrf_exempt(
            AsyncGraphQLView.as_view(
                schema=schema,
                graphiql=True,
            )
        ),
    ),
]

```

## Installation

```bash
pip install strawberry-django-phonenumber
```

### Changelog

**0.1.0**

    - Initial release


## Contributing

Running tests:

```bash
poetry run pytest
```

That's it, lite process for now. Please open a pull request or issue.
