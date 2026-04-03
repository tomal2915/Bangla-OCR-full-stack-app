from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
import os

from .models import Prediction
from .serializers import PredictionSerializer
from .ml_model import predict_image

# Accepted file extensions (content-type can lie on Windows)
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

        # Check by file extension — more reliable than content-type on Windows
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