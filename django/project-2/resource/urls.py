from django.urls import path, include
from rest_framework import routers
from resource.views import ResourceView

router = routers.DefaultRouter()
router.register(r'', ResourceView, 'resource')

urlpatterns = [
    path('', include(router.urls), name='resource'),
]
