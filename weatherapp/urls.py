from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('location_weather/', views.location_weather, name='location_weather'),
]

