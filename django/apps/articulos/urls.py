from django.urls import path, include
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('articulos', views.articulos_principal, name="articulos"),
    path('articulos/nuevo', views.nuevo),
    path('articulos/editar', views.editar),
    path('articulos/borrar', views.borrar),
    path('articulos/consultar', views.consultar),
]