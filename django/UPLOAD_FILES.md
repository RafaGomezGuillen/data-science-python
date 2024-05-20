# Uploading files in Django Rest Framework

> [!NOTE]
> Serializer, Views, URLs and admin are the same as "normal models". Check it in CREATE_API_DJANGO.md

## Create a model

Define a model in `models.py` that includes a field to store the uploaded file. Use the ImageField from Django's models module to handle image uploads.

```py
class Model(models.Model):
    image = models.ImageField(upload_to='<folder_name>/', null=True, blank=True)

    # Method to delete the file when I delete a model instance
    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)
```

Ensure that you replace `<folder_name>` with the desired folder name where uploaded images will be stored.

## Implement Signals

Implement signal methods in `signals.py` to handle file operations such as deletion of old images when updating model instances.

```py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Model

# Method to delete the old image when updating the model
@receiver(pre_save, sender=Model)
def update_model_image(sender, instance, **kwargs):
    try:
        old_model = Model.objects.get(pk=instance.pk)
        if old_model.image and old_model.image != instance.image:
            old_model.image.delete(save=False)
    except Model.DoesNotExist:
        pass
```

This signal ensures that when a model instance is updated with a new image, the old image associated with the instance is deleted.

## Updating AppConfig

Update the application configuration in apps.py to include the signals module.

```py
from django.apps import AppConfig


class modelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'model'

    def ready(self):
        import model.signals
```

Replace modelConfig and `model` with your actual application's configuration and name, respectively.

## Update URLs Configuration

In your project's `urls.py` file, ensure that media URLs are properly served during development by adding the necessary configurations.

```py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Your existing URL patterns
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

This configuration serves media files (e.g., uploaded images) during development when DEBUG mode is enabled.

## Configure Settings

In your project's `settings.py`, configure media settings to specify the location where uploaded files will be stored.

```py
INSTALLED_APPS = [
    ...
    'model.apps.ModelConfig', # instead of 'model'
]

# Media settings (determines where images will be uploaded)

MEDIA_URL = 'media/'

MEDIA_ROOT = BASE_DIR / 'media'
```