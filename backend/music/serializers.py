from rest_framework import serializers
from i18n_utils import LocalizedModelSerializerMixin
from .models import MusicWork

class MusicWorkSerializer(LocalizedModelSerializerMixin, serializers.ModelSerializer):
    localized_fields = ('title', 'description')

    class Meta:
        model = MusicWork
        fields = '__all__'