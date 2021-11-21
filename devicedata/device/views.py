from django.db.models.aggregates import Avg
from django.db import connection
from django.shortcuts import render
from django.utils import timezone
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
        items=Device.objects.all()
        agg_size=5
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
        if 'agg_size' in request.GET and request.GET['agg_size'] is not None:
            agg_size = request.GET['agg_size']
        agg_size = int(agg_size)*60
        agg_query="to_timestamp(FLOOR (EXTRACT (EPOCH FROM timestamp) / '{0}' )* {0})"
        lower_bound_interval_aggregation={
            "lower_bound": agg_query.format(agg_size)
        }
        print(lower_bound_interval_aggregation)
        # items.annotate(minute=TruncMinute('timestamp')).aggregate(Avg('reading'))
        items = items.extra(select=lower_bound_interval_aggregation).values('lower_bound','device_id','customer_id').annotate(value_avg=Avg('reading')).order_by('device_id','customer_id')
        # print(connection.queries[-1])
        each_data={}
        each_reading={}
        data=[]
        prev_device=None
        for i in items:
            each_reading["timestamp"]=i["lower_bound"]
            each_reading["reading"]=i["value_avg"]
            if i["device_id"]!=prev_device:
                readings=[]
                each_data["device_id"]=i["device_id"]
                each_data["customer_id"]=i["customer_id"]
                readings.append(each_reading.copy())
                each_data["readings"]=readings.copy()
                data.append(each_data.copy())
            else:
                each_data["readings"].append(each_reading.copy())   
            prev_device=i["device_id"]    

        serializer=DeviceResponseSerializer(data)
        return Response({'data':data},status=status.HTTP_200_OK)
