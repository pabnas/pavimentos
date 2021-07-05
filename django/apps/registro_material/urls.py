from django.urls import path, include
from . import views


urlpatterns = [
    path('registro_material', views.registro_material_home, name="registro_material"),
]