from django.urls import path, include
from rest_framework import routers
from game import views

# api versioning (GET, POST, PUT, DELETE)
router = routers.DefaultRouter()
router.register(r"", views.GameView, "game")

urlpatterns = [
    path('', include(router.urls), name="game"),
]
