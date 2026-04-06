from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from ocr.views import debug_cors, debug_paths

urlpatterns = [
    path('admin/',       admin.site.urls),
    path('api/',         include('ocr.urls')),
    path('debug/',       debug_cors),
    path('debug-paths/', debug_paths),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)