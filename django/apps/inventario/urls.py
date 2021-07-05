from django.urls import path, include
from . import views


urlpatterns = [
    path('inventario', views.inventario_principal, name="inventario"),
]
