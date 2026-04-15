from django.db import models

# Create your models here.
from django.db import models

class Prediction(models.Model):
    image       = models.ImageField(upload_to='uploads/')
    character   = models.CharField(max_length=10)
    confidence  = models.FloatField()
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.character} ({self.confidence:.1%}) — {self.created_at:%Y-%m-%d %H:%M}"