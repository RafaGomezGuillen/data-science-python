from rest_framework import serializers
from .models import Review
from game.serializer import GameSerializerGET

class ReviewSerializerGET(serializers.ModelSerializer):
    game = GameSerializerGET()

    class Meta:
        model = Review
        fields = ['id', 'title', 'description', 'score', 'game', 'image']

class ReviewSerializerPOST(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
