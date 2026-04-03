from rest_framework import serializers
from .models import Prediction

class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Prediction
        fields = ['id', 'image', 'predicted', 'confidence', 'created_at']
        read_only_fields = ['predicted', 'confidence', 'created_at']