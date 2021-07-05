from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.index,name="login"),
    path('validarlogin', views.validar_login, name="login_validate"),

    path('registro/validar', views.validar_registro, name="validar"),
    path('registro', views.registro, name="registro"),


    #path('perfil', views.perfil, name="perfil"),
    #path('perfil/actualizar', views.perfil_actualizar, name="perfil_actualizar"),
    #path('perfil/actualizar_admin', views.perfil_actualizar_admin, name="perfil_actualizar_admin"),
    #path('perfil/buscarusername', views.buscar_username, name="buscar_username"),
    #path('perfil/saveconfig', views.saveconfig),
]