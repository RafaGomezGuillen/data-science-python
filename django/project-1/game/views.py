from rest_framework import viewsets
from .serializer import GameSerializerGET, GameSerializerPOST
from .models import Game

class GameView(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    
    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return GameSerializerGET
        return GameSerializerPOST