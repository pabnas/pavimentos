from django.urls import path, include
from . import views

urlpatterns = [
    path('compras', views.compras_principal, name="compras"),
    path('compras/cargar_detalles', views.cargar_detalles),
    path('compras/get_id_nueva_compra', views.id_compra_nueva),
    path('compras/agregar_producto', views.agregar_articulo),
    path('compras/cargar_compra', views.cargar_compra),
    path('compras/cancelar_compra', views.cancelar_compra),
    path('compras/finalizar', views.finalizar),
]
