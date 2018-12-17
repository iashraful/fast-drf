from django.urls import path, include

urlpatterns = [
    path('api/', include('test_app.urls'))
]
