from rest_framework import viewsets
from .models import Review
from .serializer import ReviewSerializerGET, ReviewSerializerPOST

class ReviewView(viewsets.ModelViewSet):
    queryset = Review.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return ReviewSerializerGET
        return ReviewSerializerPOST