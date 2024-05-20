from rest_framework import viewsets
from .serializer import BookingSerializerGET, BookingSerializerPOST
from .models import Booking


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return BookingSerializerGET
        return BookingSerializerPOST
