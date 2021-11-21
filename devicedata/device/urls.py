from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from device import views
# from devicedata import device

# router=routers.DefaultRouter()
# router.register(r'device',views.DeviceViewSet,basename=Device)
schema_view = get_schema_view(
   openapi.Info(
      title="Devices API",
      default_version='v1',
      description="Envio Devices API",
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns=[
    path('',views.DeviceView.as_view(),name='device'),
    # path('docs',views.schema_view),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]