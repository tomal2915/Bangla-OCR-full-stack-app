from rest_framework import serializers
from .models import Prediction


class PredictionSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model  = Prediction
        fields = ['id', 'image_url', 'predicted', 'confidence', 'created_at']

    def get_image_url(self, obj):
        # Safely return the image URL — return None if file doesn't exist
        try:
            request = self.context.get('request')
            if obj.image and request:
                return request.build_absolute_uri(obj.image.url)
            return None
        except Exception:
            return None