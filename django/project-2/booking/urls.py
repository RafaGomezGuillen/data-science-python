from django.urls import path, include
from rest_framework import routers
from booking.views import BookingViewSet

# api versioning (GET, POST, PUT, DELETE)
router = routers.DefaultRouter()
router.register(r'', BookingViewSet, 'booking')

urlpatterns = [
    path('', include(router.urls), name='booking'),
]