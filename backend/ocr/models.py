from django.db import models

class Prediction(models.Model):
    image      = models.ImageField(upload_to='uploads/')
    predicted  = models.CharField(max_length=100)
    confidence = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.predicted} ({self.confidence:.1f}%) — {self.created_at:%Y-%m-%d %H:%M}"

    class Meta:
        ordering = ['-created_at']