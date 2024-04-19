from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Company",
        default_version='v1',
        description="Test description",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

swagger_urlpatterns = [
    path('api/v1/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='api_swagger'),
    path('api/v1/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='api_redoc'),
]
