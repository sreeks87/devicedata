from django.db.models.aggregates import Avg
from django.db import connection
from django.shortcuts import render
from django.db.models.functions import TruncMinute
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from device.models import Device
from device.serializers import DeviceRequestSerializer
from device.serializers import DeviceResponseSerializer
# Create your views here.


class DeviceView(APIView):
    
    def post(self,request):
        serializer=DeviceRequestSerializer(data=request.data,many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response("error occurred ",status=status.HTTP_400_BAD_REQUEST)
     
    def get(self,request):
        # items=Device.objects.raw('''SELECT customer_id,device_id,avg(reading) avg, 
        # to_timestamp(floor((extract('epoch' from timestamp) / 300 )) * 300) 
        # AT TIME ZONE 'UTC' as interval_alias
        # FROM device_device GROUP BY customer_id,device_id,interval_alias,id
        # ''')
        items=Device.objects.all()
        if 'customer_id' in request.GET and request.GET['customer_id'] is not None: 
            cust_id=request.GET['customer_id'] 
            items=items.filter(customer_id=cust_id)
        if 'device_id' in request.GET and request.GET['device_id'] is not None:
            dev_id=request.GET['device_id'] 
            items=items.filter(device_id=dev_id)
        if 'start_time' in request.GET and request.GET['start_time'] is not None:
            start_time=request.GET['start_time']
            items=items.filter(start_time__gt=start_time)
        if 'end_time' in request.GET and request.GET['end_time'] is not None:
            end_time=request.GET['end_time']
            items=items.filter(end_time__lt=end_time)
        # items.annotate(minute=TruncMinute('timestamp')).aggregate(Avg('reading'))
        items = items.extra(select={'interval': "FLOOR (EXTRACT (EPOCH FROM timestamp) / '300' )* 300"}).values('interval','customer_id','device_id').annotate(value_avg=Avg('reading'))
        print(connection.queries[-1])
        print(items)
        serializer=DeviceResponseSerializer(items,many=True)
        return Response({'data':serializer.data},status=status.HTTP_200_OK)




# Dummy Request
# [{
# "timestamp": "2021-11-20T14:29:43+00:00",
# "reading": 12.35,
# "device_id": "23706ac3-88c4-45a4-9ca0-427d7f162cdb",
# "customer_id": "2140c6cf-f513-489c-b49f-a8686582c664"
# }]

# {'interval': Decimal('1637418300'), 'customer_id': UUID('2140c6cf-f513-489c-b49f-a8686582c664'), 'device_id': UUID('23706ac3-88c4-45a4-9ca0-427d7f162cdb'), 'value_avg': 29.005}, 
# {'interval': Decimal('1637418300'), 'customer_id': UUID('2140c6cf-f513-489c-b49f-a8686582c664'), 'device_id': UUID('d91c3e70-e642-430d-bbb8-9f190cf1df3c'), 'value_avg': 3050.1433333333334}, 
# {'interval': Decimal('1637418300'), 'customer_id': UUID('c39f43c5-ce76-4b77-993a-f13dfdc5ece1'), 'device_id': UUID('d91c3e70-e642-430d-bbb8-9f190cf1df3c'), 'value_avg': 12.35}, 
# {'interval': Decimal('1637418300'), 'customer_id': UUID('5866c3e9-89cf-4955-b7cc-b39762af5d0c'), 'device_id': UUID('1dae7442-a8ac-47d8-83f9-70672cdb0694'), 'value_avg': 12.35}, 
# {'interval': Decimal('1637418600'), 'customer_id': UUID('2140c6cf-f513-489c-b49f-a8686582c664'), 'device_id': UUID('23706ac3-88c4-45a4-9ca0-427d7f162cdb'), 'value_avg': 347.3766666666666}, 
# {'interval': Decimal('1637418000'), 'customer_id': UUID('2140c6cf-f513-489c-b49f-a8686582c664'), 'device_id': UUID('23706ac3-88c4-45a4-9ca0-427d7f162cdb'), 'value_avg': 1367.7199999999998}