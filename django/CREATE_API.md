# Creating API the Old-Fashioned Way

## Creating a Model

In your `models.py` file, define the `Task` model as follows:

```py
from django.db import models
from django.core.validators import MinLengthValidator


class Task(models.Model):
    title = models.CharField(max_length=200, validators=[MinLengthValidator(
        3, "The task must be between 3 and 200 characters long.")])

    description = models.TextField(null=True, blank=True, validators=[MinLengthValidator(
        3, "The task must be at least 3 characters long.")])

    complete = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.title}"
```

## Create View

Define a **ModelkView** in your `views.py` file to handle CRUD operations:

```py
from typing import Any
from django.http.response import HttpResponse as HttpResponse
from django.views import View
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Task

class TaskView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk=0):
        pass

    def post(self, request):
        pass

    def put(self, request, pk=0):
        pass

    def delete(self, request, pk=0):
        pass
```

### Handling GET Method

```py
def get(self, request, pk=0):
    if (pk == 0):
        tasks = list(Task.objects.values())

        if tasks:
            message = {
                'message': 'success',
                'tasks': tasks
            }
        else:
            message = {
                'message': 'No tasks registered',
            }
    else:
        tasks = list(Task.objects.filter(id=pk).values())

        if tasks:
            task = tasks[0]
            message = {
                'message': 'success',
                'tasks': task
            }
        else:
            message = {
                'message': f'No tasks registered with id: {pk}',
            }

    return JsonResponse(message)
```

### Handling POST Method

```py
def post(self, request):
    js = json.loads(request.body)

        Task.objects.create(
            title=js['title'],
            description=js['description'],
            complete=js['complete']
        )

        message = {
            'message': 'Task created'
        }

        return JsonResponse(message)
```

### Handling PUT Method

```py
def put(self, request, pk=0):
    js = json.loads(request.body)
    tasks = list(Task.objects.filter(id=pk).values())

    if tasks:
        task = Task.objects.get(id=pk)

        task.title = js['title']
        task.description = js['description']
        task.complete = js['complete']

        task.save()

        message = {
            'message': f'Task with {pk} updated'
        }
    else:
        message = {
            'message': f'No tasks registered with id: {pk}'
        }

    return JsonResponse(message)
```

### Handling DELETE Method

```py
def delete(self, request, pk=0):
    tasks = list(Task.objects.filter(id=pk).values())

    if tasks:
        Task.objects.filter(id=pk).delete()

        message = {
            'message': f'Task with {pk} deleted'
        }
    else:
        message = {
            'message': f'No tasks registered with id: {pk}'
        }

    return JsonResponse(message)
```

## Defining app and enviroment URLs

In your `urls.py ` file, define the URLs for your app:

```py
from django.urls import path
from task import views

urlpatterns = [
    path('', views.TaskView.as_view(), name="task_list"),
    path('<int:pk>', views.TaskView.as_view(), name="task_details"),
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