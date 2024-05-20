from django.db import models
from django.contrib.auth.models import User
from resource.models import Resource


class Booking(models.Model):
    RESOURCE_TYPE = [
        ('RE', 'Requested'),
        ('GR', 'Granted'),
        ('US', 'Used'),
        ('FI', 'Finantial'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.DateField()
    end_time = models.DateField()
    status = models.CharField(
        max_length=2, choices=RESOURCE_TYPE, default='RE')
    
    def __str__(self) -> str:
        return f'{self.user}: {self.resource}'
