from rest_framework import serializers
from .models import FallDetectionData

class FallDetectionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FallDetectionData
        fields = '__all__'