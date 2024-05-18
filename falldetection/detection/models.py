from django.db import models

class FallDetectionData(models.Model):
    sample_num = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    predicted_activity = models.CharField(max_length=20)
    accel_x = models.FloatField(default=0)
    accel_y = models.FloatField(default=0)
    accel_z = models.FloatField(default=0)

    def __str__(self):
        return f"Fall Detection Data at {self.timestamp}"