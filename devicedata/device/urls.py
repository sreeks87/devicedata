from django.db.models import base
from django.urls import include,path
from rest_framework import routers, urlpatterns
from device import views
from device.models import Device
# from devicedata import device

# router=routers.DefaultRouter()
# router.register(r'device',views.DeviceViewSet,basename=Device)


urlpatterns=[
    path('',views.DeviceView.as_view()),
]