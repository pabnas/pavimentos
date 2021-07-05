from django.urls import path, include
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('proveedores', views.proveedores_principal, name="proveedores"),
    path('proveedores/nuevo', views.nuevo),
    path('proveedores/editar', views.editar),
    path('proveedores/borrar', views.borrar),
]