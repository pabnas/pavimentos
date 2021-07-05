from django.urls import path, include
from . import views

urlpatterns = [
    path('ventas', views.ventas_principal, name="ventas"),
    path('ventas/cargar_detalles', views.cargar_detalles),
    path('ventas/get_id_nueva_venta', views.id_venta_nueva),
    path('ventas/agregar_producto', views.agregar_articulo),
    path('ventas/cargar_venta', views.cargar_venta),
    path('ventas/cancelar_venta', views.cancelar_venta),
    path('ventas/finalizar', views.finalizar),
]
