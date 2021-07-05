from django.urls import path, include
from . import views


urlpatterns = [
    path('requision', views.requision_home, name="requision"),
]