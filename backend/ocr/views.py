import os
import io
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse
from django.conf import settings
from django.core.files.base import ContentFile
from PIL import Image

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

        # Read the raw bytes once — avoids seek() issues with cloud storage
        raw_bytes = image_file.read()

        # Run ML prediction from bytes
        try:
            predicted_label, confidence = predict_image(
                io.BytesIO(raw_bytes)
            )
        except Exception as e:
            return Response(
                {'error': f'Prediction failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Convert to PNG for browser compatibility
        try:
            pil_img    = Image.open(io.BytesIO(raw_bytes)).convert('RGB')
            png_buffer = io.BytesIO()
            pil_img.save(png_buffer, format='PNG')
            png_bytes  = png_buffer.getvalue()
        except Exception as e:
            return Response(
                {'error': f'Image conversion failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Build PNG file for storage
        base_name    = os.path.splitext(image_file.name)[0]
        png_filename = base_name + '.png'
        png_file     = ContentFile(png_bytes, name=png_filename)

        # Save to database
        try:
            prediction = Prediction.objects.create(
                image      = png_file,
                predicted  = predicted_label,
                confidence = confidence,
            )
        except Exception as e:
            return Response(
                {'error': f'Database save failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
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


def debug_cors(request):
    return JsonResponse({
        'CORS_ALLOWED_ORIGINS': settings.CORS_ALLOWED_ORIGINS,
        'CORS_ALLOW_ALL_ORIGINS': settings.CORS_ALLOW_ALL_ORIGINS,
        'DEBUG': settings.DEBUG,
        'ALLOWED_HOSTS': settings.ALLOWED_HOSTS,
    })