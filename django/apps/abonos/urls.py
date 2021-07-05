from django.urls import path, include
from . import views


urlpatterns = [
    path('abonos', views.abonos_home, name="abonos"),
]