from rest_framework import serializers
from .models import Prediction

class PredictionSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Prediction
        fields = ['id', 'image', 'predicted', 'confidence', 'created_at']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            # Force HTTPS scheme
            url = obj.image.url
            if request.is_secure():
                return url.replace('http://', 'https://')
            return request.build_absolute_uri(url)
        return None