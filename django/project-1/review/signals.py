# signals.py

from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Review

@receiver(pre_save, sender=Review)
def update_review_image(sender, instance, **kwargs):
    try:
        old_review = Review.objects.get(pk=instance.pk)
        if old_review.image and old_review.image != instance.image:
            old_review.image.delete(save=False)
    except Review.DoesNotExist:
        pass
