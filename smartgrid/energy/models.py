from django.db import models
from django.contrib.auth.models import User

class EnergyRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    kwh_usage = models.FloatField()  # Kilowatt-hours consumed
    cost = models.FloatField()       # Estimated cost

    def __str__(self):
        return f"{self.user.username} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
