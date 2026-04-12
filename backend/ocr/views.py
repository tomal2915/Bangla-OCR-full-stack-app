# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Prediction
from .serializers import PredictionSerializer
from .predictor import predict_character


class PredictView(APIView):
    def post(self, request):
        image_file = request.FILES.get('image')

        if not image_file:
            return Response(
                {'error': 'No image provided. Send image as multipart/form-data with key "image".'},
                status=status.HTTP_400_BAD_REQUEST
            )

        allowed_types = ['image/png', 'image/jpeg', 'image/jpg', 'image/bmp']
        if image_file.content_type not in allowed_types:
            return Response(
                {'error': f'Unsupported file type: {image_file.content_type}. Use PNG or JPG.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if image_file.size > 5 * 1024 * 1024:
            return Response(
                {'error': 'Image too large. Maximum size is 5MB.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            character, confidence = predict_character(image_file)
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Prediction failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        prediction = Prediction.objects.create(
            image      = image_file,
            character  = character,
            confidence = confidence,
        )

        return Response({
            'character'         : character,
            'confidence'        : confidence,
            'confidence_percent': f"{confidence * 100:.1f}%",
            'id'                : prediction.id,
        }, status=status.HTTP_201_CREATED)


class PredictionHistoryView(APIView):
    def get(self, request):
        # no try/except here — let Django show the real error
        predictions = Prediction.objects.all()[:20]
        serializer  = PredictionSerializer(predictions, many=True)
        return Response(serializer.data)