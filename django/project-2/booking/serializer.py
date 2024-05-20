from rest_framework import serializers
from .models import Booking
from resource.serializer import ResourceSerializer
from user_api.serializer import UserSerializer


class BookingSerializerGET(serializers.ModelSerializer):
    resource = ResourceSerializer()
    user = UserSerializer()

    class Meta:
        model = Booking
        fields = ['user', 'resource', 'start_date',
                  'end_date', 'start_time', 'end_time', 'status']


class BookingSerializerPOST(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
