from django.urls import path, include
from rest_framework import routers
from review import views

# api versioning (GET, POST, PUT, DELETE)
router = routers.DefaultRouter()
router.register(r"", views.ReviewView, "review")

urlpatterns = [
    path('', include(router.urls), name="review"),
]
