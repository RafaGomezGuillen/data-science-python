# Creating API with Serializers

## Create a model

Create model in `models.py`

```py
from django.db import models
from django.core.validators import MinLengthValidator
from genre.models import Genre

class Game(models.Model):
    name = models.CharField(max_length=30, validators=[MinLengthValidator(
        3, "The name must be between 3 and 30 characters long.")])
    # The game has one genre. If I delete his genre the game will automatically delete as well
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name}"
```

## Create serializer file

Create `serializer.py`. File where you define the way backend send models and fields to frontend.

> [!NOTE]
> If the model does not have another relation to another one the ModelSerializer could be like this.

```py
from rest_framework import serializers
from .models import ModelName

class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelName # You have to import the model as well
        # fields = ("id", "title", "description", "isDone") # Import specific fields
        fields = "__all__" # Import all fields
```

> [!NOTE]
> If the model does have another relation to another one the ModelSerializer could be like this.

```py
from rest_framework import serializers
from .models import Model
from model2.serializer import Model2Serializer


class ModelSerializerGET(serializers.ModelSerializer):
    Model2 = Model2Serializer()

    class Meta:
        model = Model
        fields = ['field', 'field', 'Model2']


class ModelSerializerPOST(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = '__all__'
```

## Queryset and view API

Create a class view to the created model in views.py

> [!WARNING]
> serializer_class and queryset var names could not be other than that.

> [!NOTE]
> If the model does not have another relation to another one the ModelSerializer could be like this.

```py
from rest_framework import viewsets
from .serializer import ModelSerializer
from .models import ModelName

class ModelView(viewsets.ModelViewSet):
    serializer_class = ModelSerializer
    queryset = ModelName.objects.all()
```

> [!NOTE]
> If the model does have another relation to another one the ModelSerializer could be like this.

```py
from rest_framework import viewsets
from .serializer import ModelSerializerGET, ModelSerializerPOST
from .models import Model

class ModelViewSet(viewsets.ModelViewSet):
    queryset = Model.objects.all()
    
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return ModelSerializerGET
        return ModelSerializerPOST
```

## Defining app and enviroment URLs

1. Create `urls.py`

```py
from django.urls import path, include
from rest_framework import routers
from <app_name> import views

# api versioning (GET, POST, PUT, DELETE)
router = routers.DefaultRouter()
router.register(r'', views.TaskView, 'model_name')

urlpatterns = [
    path('', include(router.urls), name='model_name'),
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
    path('api/model_name/', include("<app_name>.urls"))
]
```

## Add a model to Admin page

- In `app/admin.py` add:

```py
from .models import <model>
# Register your models here.
admin.site.register(<model>)
```

## Data migration to DB

Migrate a created or modified model to app/migrations/file.py.

```cmd
python manage.py makemigrations <name_app>
```

Migrate the existing tables to database.

```cmd
python manage.py migrate <app>
```
