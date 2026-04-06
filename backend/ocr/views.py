import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse
from django.conf import settings

from .models import Prediction
from .serializers import PredictionSerializer
from .ml_model import predict_image

ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.bmp'}


class PredictView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        if 'image' not in request.FILES:
            return Response(
                {'error': 'No image provided. Send a file with key "image".'},
                status=status.HTTP_400_BAD_REQUEST
            )

        image_file = request.FILES['image']
        ext = os.path.splitext(image_file.name)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            return Response(
                {'error': f'Invalid file type: {ext}. Send PNG, JPEG, or BMP.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            predicted_label, confidence = predict_image(image_file)
        except Exception as e:
            return Response(
                {'error': f'Prediction failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        prediction = Prediction.objects.create(
            image      = image_file,
            predicted  = predicted_label,
            confidence = confidence,
        )
        serializer = PredictionSerializer(
            prediction,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PredictionHistoryView(APIView):
    def get(self, request):
        predictions = Prediction.objects.all()[:20]
        serializer  = PredictionSerializer(
            predictions,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)


# ── Temporary debug endpoint ──────────────────────────────────
# Visit /debug/ on Railway to confirm env vars are loaded correctly
# Remove this view and its url entry once CORS is confirmed working
def debug_cors(request):
    return JsonResponse({
        'CORS_ALLOWED_ORIGINS': settings.CORS_ALLOWED_ORIGINS,
        'CORS_ALLOW_ALL_ORIGINS': settings.CORS_ALLOW_ALL_ORIGINS,
        'DEBUG': settings.DEBUG,
        'ALLOWED_HOSTS': settings.ALLOWED_HOSTS,
    })