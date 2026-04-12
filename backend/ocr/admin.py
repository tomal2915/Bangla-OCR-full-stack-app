from django.contrib import admin
from .models import Prediction

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display  = ['character', 'confidence', 'created_at']
    list_filter   = ['character']
    ordering      = ['-created_at']