from django.urls import path, include
from . import views

urlpatterns = [
    path('clientes', views.clientes_principal, name="clientes"),
    path('clientes/nuevo', views.nuevo),
    path('clientes/editar', views.editar),
    path('clientes/borrar', views.borrar),
    path('clientes/consultar', views.consultar),
]
