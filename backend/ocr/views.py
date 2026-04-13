from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Prediction
from .serializers import PredictionSerializer
from .predictor import predict_character

ALLOWED_TYPES = {'image/png', 'image/jpeg', 'image/jpg', 'image/bmp'}
MAX_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB


class PredictView(APIView):
    """
    POST /api/predict/
    multipart/form-data — key: 'image'
    """

    def post(self, request):
        image_file = request.FILES.get('image')

        if not image_file:
            return Response(
                {'error': 'No image provided. Send image as multipart/form-data with key "image".'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if image_file.content_type not in ALLOWED_TYPES:
            return Response(
                {'error': f'Unsupported type: {image_file.content_type}. Use PNG or JPG.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if image_file.size > MAX_SIZE_BYTES:
            return Response(
                {'error': 'Image too large. Maximum size is 5 MB.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            character, confidence = predict_character(image_file)
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception:
            return Response(
                {'error': 'Prediction failed. Please try again.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        prediction = Prediction.objects.create(
            image      = image_file,
            character  = character,
            confidence = confidence,
        )

        return Response(
            {
                'id'                : prediction.id,
                'character'         : character,
                'confidence'        : confidence,
                'confidence_percent': f"{confidence * 100:.1f}%",
            },
            status=status.HTTP_201_CREATED,
        )


class PredictionHistoryView(APIView):
    """
    GET /api/predictions/
    Returns last 20 predictions.
    """

    def get(self, request):
        predictions = Prediction.objects.all()[:20]
        serializer  = PredictionSerializer(predictions, many=True)
        return Response(serializer.data)