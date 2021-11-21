from django.db.models.aggregates import Avg
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from device.models import Device
from device.serializers import DeviceRequestSerializer
from device.serializers import DeviceSingleResponseSerializer
# Create your views here.
from rest_framework_swagger.views import get_swagger_view


class DeviceView(APIView):
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'device_id': openapi.Schema(type=openapi.TYPE_STRING, description='The device ID'),
            'customer_id': openapi.Schema(type=openapi.TYPE_STRING, description='The customer ID'),
            'timestamp': openapi.Schema(type=openapi.TYPE_STRING, description='The timestamp of the generated data'),
            'reading': openapi.Schema(type=openapi.TYPE_STRING, description='The reading from the device'),
        }))
    def post(self,request):
        '''
    The POST method acceps a reading rom a device.
    Expects an array of the defined schema
    '''
        serializer=DeviceRequestSerializer(data=request.data,many=True)
        print("----------------Request--------------")
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            print(str(serializer.errors))
            return Response("error occurred :"+str(serializer.errors) ,status=status.HTTP_400_BAD_REQUEST)

    def get(self,request):
        '''
    The GET method retuns the aggregated data from a device over a period of 5 mins(default)
    This default aggregate_size can be modified with a query param agg_size
    Accepted query params: 
    device_id (example 23706ac3-88c4-45a4-9ca0-427d7f162cdb)
    customer_id (example 2140c6cf-f513-489c-b49f-a8686582c664)
    start_time (example start_time=2021-11-20T14:25:00Z; defaults to no lower limit if notpresent)
    end_time (example start_time=2021-11-20T14:25:00Z; defaults to no upper limit if not present)
    agg_size (example 10)
    http://127.0.0.1:8000/device/?device_id=23706ac3-88c4-45a4-9ca0-427d7f162cdb&agg_size=10
    http://127.0.0.1:8000/device/?customer_id=23706ac3-88c4-45a4-9ca0-427d7f162cdb
    
        '''  
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
            items=items.filter(timestamp__gt=start_time)
        if 'end_time' in request.GET and request.GET['end_time'] is not None:
            end_time=request.GET['end_time']
            items=items.filter(timestamp__lt=end_time)
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

        serializer=DeviceSingleResponseSerializer(data=data,many=True)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response({'data':serializer.errors},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'data':serializer.data},status=status.HTTP_200_OK)
