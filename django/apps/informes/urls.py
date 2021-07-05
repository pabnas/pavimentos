from django.urls import path, include
from . import views


urlpatterns = [
    path('informes', views.informes_principal, name="informes"),
]