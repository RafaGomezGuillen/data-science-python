# User Authentification and Authorization

## Create User app

Without creating any User Model. We are going to use the default User Model from Django.

## Create serializer file

Create `serializer.py`. File where you define the way backend send models and fields to frontend.

```py
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 'is_staff']
```

## Queryset and view API

Create a class view to the created model in views.py

```py
from rest_framework import viewsets
from .serializer import UserSerializer
from django.contrib.auth.models import User


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
```

## Defining app and enviroment URLs

1. Create `urls.py`

```py
from django.urls import path, include
from rest_framework import routers
from user_api.views import UserView

router = routers.DefaultRouter()
router.register(r'', UserView, 'user')

urlpatterns = [
    path('', include(router.urls), name='user'),
]
```

2. In `<project_name>/urls.py`

```py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('api/', permanent=True)),
    path('admin/', admin.site.urls),
    path('api/user/', include('user_api.urls')),
]
```