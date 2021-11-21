from django.db import models

# Create your models here.

class Device(models.Model):
    # not expected to be blank
    timestamp = models.DateTimeField()
    reading = models.FloatField()
    device_id = models.UUIDField()
    customer_id = models.UUIDField()
