from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [path("", include("fast_drf.tests.test_app.urls"))]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
