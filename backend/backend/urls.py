from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from ocr.views import debug_cors

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',   include('ocr.urls')),
    path('debug/', debug_cors),          # remove after confirming CORS works
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)