from django.urls import path, include
from rest_framework import routers
from user_api.views import UserView

router = routers.DefaultRouter()
router.register(r'', UserView, 'user')

urlpatterns = [
    path('', include(router.urls), name='user'),
]
