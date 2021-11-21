from django.test import TestCase
from django.urls import reverse

from device.models import Device
class DeviceAPIViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Device.objects.create(device_id="1dae7442-a8ac-47d8-83f9-70672cdb0694",customer_id="1dae7442-a8ac-47d8-83f9-70672cdb0694",timestamp="2021-11-20T14:25:00Z",reading="158.323")

    def test_get(self):
        data=self.client.get(reverse('deviceapi'))
        print(data.content)
        self.assertEqual(data.status_code,200)

    def test_post(self):
        data=self.client.post(reverse('deviceapi'),[{
            "device_id": "1dae7442-a8ac-47d8-83f9-70672cdb0694",
            "customer_id": "5866c3e9-89cf-4955-b7cc-b39762af5d0c",
            "timestamp":"2021-11-20T14:25:00Z",
            "reading":"56.32"
        }],follow=True,content_type="application/json")
        print(data.status_code)
        self.assertEqual(data.status_code,201)

    def test_post400(self):
        data=self.client.post(reverse('deviceapi'),[{
            "device_id": "",
            "customer_id": "wewqfwfwf",
            "timestamp":"2021-11-20T14:25:00Z",
            "reading":"56.32"
        }],follow=True,content_type="application/json")
        print(data.status_code)
        self.assertEqual(data.status_code,400)

    def test_post400_reading(self):
        data=self.client.post(reverse('deviceapi'),[{
            "device_id": "1dae7442-a8ac-47d8-83f9-70672cdb0694",
            "customer_id": "1dae7442-a8ac-47d8-83f9-70672cdb0694",
            "timestamp":"2021-11-20T14:25:00Z",
            "reading":""
        }],follow=True,content_type="application/json")
        print(data.status_code)
        self.assertEqual(data.status_code,400)

    def test_post400_reading(self):
        data=self.client.post(reverse('deviceapi'),[{
            "device_id": "1dae7442-a8ac-47d8-83f9-70672cdb0694",
            "customer_id": "1dae7442-a8ac-47d8-83f9-70672cdb0694",
            "timestamp":"",
            "reading":"53.65"
        }],follow=True,content_type="application/json")
        print(data.status_code)
        self.assertEqual(data.status_code,400)