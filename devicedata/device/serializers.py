from django.db.models import fields
from rest_framework import serializers

from device.models import Device


class DeviceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model=Device
        fields=['timestamp','reading','device_id','customer_id']

class ReadingSerializer(serializers.Serializer):
    timestamp=serializers.DateTimeField()
    reading=serializers.FloatField

class DeviceResponseSerializer(serializers.Serializer):
    device_id=serializers.UUIDField()
    customer_id=serializers.UUIDField()
    readings=ReadingSerializer(many=True)

