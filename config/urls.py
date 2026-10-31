from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from config import settings

schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="My API",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


    path('admin/', admin.site.urls),
    path('api/v1/', include(
        [
            path("auth/", include("accounts.urls")),
            path("apps/", include("apps.urls")),
            path("task/", include("task.urls")),
        ]
    ))

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)