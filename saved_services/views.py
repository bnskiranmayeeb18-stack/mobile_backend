from rest_framework import viewsets
from .models import SavedService
from .serializers import SavedServiceSerializer

class SavedServiceViewSet(viewsets.ModelViewSet):
    queryset = SavedService.objects.all()
    serializer_class = SavedServiceSerializer