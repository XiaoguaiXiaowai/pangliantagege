from rest_framework import serializers
from .models import MusicWork

class MusicWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicWork
        fields = '__all__'
