from django.db import models
from django.contrib.auth.models import User


class Resource(models.Model):
    RESOURCE_TYPE = [
        ('HU', 'Human'),
        ('FI', 'Finantial'),
        ('MA', 'Material'),
        ('TE', 'Technical'),
    ]

    name = models.CharField(max_length=50)
    description = models.TextField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=2, choices=RESOURCE_TYPE, default='MA')

    def __str__(self) -> str:
        return f'{self.name}'
