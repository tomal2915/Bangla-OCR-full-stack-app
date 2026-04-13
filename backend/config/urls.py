from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse


def health(request):
    return JsonResponse({'status': 'ok'})


urlpatterns = [
    path('admin/',   admin.site.urls),
    path('api/',     include('ocr.urls')),
    path('health/',  health),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)