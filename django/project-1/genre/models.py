from django.db import models
from django.core.validators import MinLengthValidator


class Genre(models.Model):
    title = models.CharField(max_length=30, validators=[MinLengthValidator(3, "The title must be between 3 and 30 characters long.")])

    def __str__(self) -> str:
        return f"{self.title}"
