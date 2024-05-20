from rest_framework import serializers
from .models import Game
from genre.serializer import GenreSerializer


class GameSerializerGET(serializers.ModelSerializer):
    genre = GenreSerializer()

    class Meta:
        model = Game
        fields = ['id', 'name', 'genre']


class GameSerializerPOST(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'
