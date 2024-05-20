from django.db import models
from django.core.validators import MinLengthValidator
from genre.models import Genre

class Game(models.Model):
    name = models.CharField(max_length=30, validators=[MinLengthValidator(
        3, "The name must be between 3 and 30 characters long.")])
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name}"
