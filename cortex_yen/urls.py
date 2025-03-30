from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authentication import TokenAuthentication
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import os

schema_view = get_schema_view(
    openapi.Info(
        title="Cortex Yen API",
        default_version="v1",
        description="API documentation for Cortex Yen",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourdomain.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(TokenAuthentication,),  # Add this line
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("cortex_yen_app.urls")),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("swagger.json", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    # Explicit media URL pattern that works in both debug and production
    path('media/<path:path>', serve, {
        'document_root': os.path.join(settings.BASE_DIR, 'media'),
    }),
]

# Serve media files in development (alternative method)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
