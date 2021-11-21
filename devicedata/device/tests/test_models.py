from django.test import TestCase

from device.models import Device

class DeviceModelTest(TestCase):
    @classmethod
    def setup(cls):
        Device.objects.create(device_id="1dae7442-a8ac-47d8-83f9-70672cdb0694",customer_id="1dae7442-a8ac-47d8-83f9-70672cdb0694",timestamp="2021-11-20T14:25:00Z",reading="158.323")

    def label_device_id(self):
        d=Device.objects.get(id=1)
        f=d._meta.get_field('device_id').verbose_name
        self.assertEqual(f,'device_id')

    def label_customer_id(self):
        d=Device.objects.get(id=1)
        f=d._meta.get_field('customer_id').verbose_name
        self.assertEqual(f,'customer_id')


    def label_timestamp(self):
        d=Device.objects.get(id=1)
        f=d._meta.get_field('timestamp').verbose_name
        self.assertEqual(f,'timestamp')


    def label_reading(self):
        d=Device.objects.get(id=1)
        f=d._meta.get_field('reading').verbose_name
        self.assertEqual(f,'reading')


