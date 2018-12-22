from django.urls import path, include

urlpatterns = [
    path('api/', include('example_app.urls'))
]
