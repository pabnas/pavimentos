from django.urls import path, include
from . import views


urlpatterns = [
    path('empresas', views.empresas_principal, name="empresas"),
    path('empresas/editar', views.editar_empresa),
    path('empresas/miembro/agregar', views.agregar),
    path('empresas/miembro/eliminar', views.empresas_principal),
    path('empresas/miembro/editar', views.editar_miembro),
]
