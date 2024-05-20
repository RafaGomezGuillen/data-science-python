from rest_framework import viewsets
from .serializer import GenreSerializer
from .models import Genre

class GenreView(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()