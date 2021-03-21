from django.urls import path, include

urlpatterns = [
    path('', include('fast_drf.tests.test_app.urls'))
]
