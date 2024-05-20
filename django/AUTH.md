# Token Authentication in Django REST Framework

## Installation

Add the rest_framework.authtoken app to the INSTALLED_APPS list in your `settings.py` file:

```py
INSTALLED_APPS = [
    'rest_framework.authtoken'
]
```

## Migration

Generate a new migration to create the necessary table in the database:

```cmd
python manage.py makemigrations
python manage.py migrate
```

## Configuration

In your `settings.py`, configure the default permission classes to allow read-only access for unidentified users:

```py
REST_FRAMEWORK = {
  'DEFAULT_PERMISSION_CLASSES': [
    'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
  ]
}
```

## Restricting Access

To restrict access to certain views to only authenticated users, use the `IsAuthenticated` permission class:

```py
from rest_framework.permissions import IsAuthenticated

class ResourceView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
```

## Generating Tokens

To generate tokens for users, configure the user view with `TokenAuthentication`:

```py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializer import UserSerializer
from django.contrib.auth.models import User


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
```

## Admin Views for Tokens

To manage tokens in the Django admin interface, you can add the token table:

```py
from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ['user']
```
