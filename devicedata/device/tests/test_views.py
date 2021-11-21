from django.http import response
from django.test import TestCase
from django.urls import reverse

from device.models import Device
class DeviceAPIViewTest(TestCase):
    @classmethod
    def setup(cls):
        Device.objects.create(device_id="1dae7442-a8ac-47d8-83f9-70672cdb0694",customer_id="1dae7442-a8ac-47d8-83f9-70672cdb0691",timestamp="2021-11-20T14:25:00Z",reading="158.323")
        Device.objects.create(device_id="1dae7442-a8ac-47d8-83f9-70672cdb0693",customer_id="1dae7442-a8ac-47d8-83f9-70672cdb0692",timestamp="2021-11-20T14:35:00Z",reading="138.323")
        Device.objects.create(device_id="1dae7442-a8ac-47d8-83f9-70672cdb0692",customer_id="1dae7442-a8ac-47d8-83f9-70672cdb0693",timestamp="2021-11-20T14:45:00Z",reading="148.323")
        Device.objects.create(device_id="1dae7442-a8ac-47d8-83f9-70672cdb0691",customer_id="1dae7442-a8ac-47d8-83f9-70672cdb0694",timestamp="2021-11-20T14:55:00Z",reading="185.323")
        Device.objects.create(device_id="1dae7442-a8ac-47d8-83f9-70672cdb0690",customer_id="1dae7442-a8ac-47d8-83f9-70672cdb0695",timestamp="2021-11-20T14:65:00Z",reading="358.323")
    
    def test_get(self):
        data=self.client.get(reverse('device'))
        self.assertEqual(data.status_code,200)

    def test_post(self):
        data=self.client.post(reverse('device'),{
            "device_id": "1dae7442-a8ac-47d8-83f9-70672cdb0694",
            "customer_id": "5866c3e9-89cf-4955-b7cc-b39762af5d0c",
            "teimestamp":"2021-11-20T14:25:00Z",
            "reading":"56.32"
        })
        self.assertEqual(data.status_code,201)

    def test_post400(self):
        data=self.client.post(reverse('device'),{
            "device_id": "",
            "customer_id": "wewqfwfwf",
            "teimestamp":"2021-11-20T14:25:00Z",
            "reading":"56.32"
        })
        self.assertEqual(data.status_code,400)


