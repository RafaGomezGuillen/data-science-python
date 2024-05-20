from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializer import ResourceSerializer
from .models import Resource


class ResourceView(viewsets.ModelViewSet):
    serializer_class = ResourceSerializer
    queryset = Resource.objects.all()

    permission_classes = [IsAuthenticated]