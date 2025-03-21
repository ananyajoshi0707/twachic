from django.db import models

class SkinAnalysis(models.Model):
    image = models.ImageField(upload_to='skin_images/')
    condition = models.TextField(null=True, blank=True)  # Updated from CharField to TextField
    recommendations = models.TextField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.condition[:50] if self.condition else "Pending Analysis"

