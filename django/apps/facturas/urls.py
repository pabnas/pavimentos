from django.urls import path, include
from . import views


urlpatterns = [
    path('factura', views.facturas_principal, name="factura"),
    path('factura/consultar_factura', views.consultar),
]
