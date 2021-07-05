from django.urls import path, include
from . import views


urlpatterns = [
    path('orden_de_compra', views.orden_home, name="orden_de_compra"),
]