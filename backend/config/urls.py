# urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def api_root(request):
    return Response({
        'message' : 'Bangla OCR API is running',
        'version' : '1.0',
        'endpoints': {
            'predict'    : '/api/predict/',
            'predictions': '/api/predictions/',
            'admin'      : '/admin/',
        }
    })

urlpatterns = [
    path('',       api_root,              name='api-root'),
    path('admin/', admin.site.urls),
    path('api/',   include('ocr.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)