from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import MusicWork
from .serializers import MusicWorkSerializer

class MusicWorkList(generics.ListAPIView):
    queryset = MusicWork.objects.all()
    serializer_class = MusicWorkSerializer
    permission_classes = [AllowAny]
