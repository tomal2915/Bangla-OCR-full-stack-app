# serializers.py
from rest_framework import serializers
from .models import Prediction

class PredictionSerializer(serializers.ModelSerializer):
    confidence_percent = serializers.SerializerMethodField()

    class Meta:
        model  = Prediction
        fields = [
            'id',
            'character',
            'confidence',
            'confidence_percent',
            'created_at',
        ]

    def get_confidence_percent(self, obj):
        return f"{obj.confidence * 100:.1f}%"