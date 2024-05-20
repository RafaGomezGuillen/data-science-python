from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator
from game.models import Game


class Review(models.Model):
    title = models.CharField(max_length=100, validators=[MinLengthValidator(
        3, "The title must be between 3 and 100 characters long.")])
    description = models.CharField(max_length=500, validators=[MinLengthValidator(
        10, "The description must be between 10 and 500 characters long.")])
    score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)])
    image = models.ImageField(upload_to='reviews/', null=True, blank=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.title}"