from django.db import models

class FallDetection(models.Model):
    sample_num = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    predicted_activity = models.CharField(max_length=20)
    accel_x = models.FloatField()
    accel_y = models.FloatField()
    accel_z = models.FloatField()

    def __str__(self):
        return f"Fall Detection - Sample: {self.sample_num} - Timestamp: {self.timestamp}"