from django.urls import path
from .views import (
    PredictView,
    PredictionHistoryView,
    debug_cors,
    debug_paths,
)

urlpatterns = [
    path('predict/',      PredictView.as_view(),           name='predict'),
    path('predictions/',  PredictionHistoryView.as_view(), name='history'),

    # Temporary debug endpoints — remove before final production
    path('debug-cors/',   debug_cors,                      name='debug-cors'),
    path('debug-paths/',  debug_paths,                     name='debug-paths'),
]