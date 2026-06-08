from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('location_weather/', views.location_weather, name='location_weather'),
    path('sw.js', views.ServiceWorkerView.as_view(), name='sw.js'),
]

