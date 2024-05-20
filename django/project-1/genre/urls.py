from django.urls import path, include
from rest_framework import routers
from genre import views

# api versioning (GET, POST, PUT, DELETE)
router = routers.DefaultRouter()
router.register(r"", views.GenreView, "genre")

urlpatterns = [
    path('', include(router.urls), name="genre"),
]
