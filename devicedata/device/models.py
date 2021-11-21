from django.db import models

# Create your models here.

class Device(models.Model):
    timestamp = models.DateTimeField(blank=False)
    reading = models.FloatField(blank=False)
    device_id = models.UUIDField(blank=False)
    customer_id = models.UUIDField(blank=False)
