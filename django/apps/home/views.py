from django.shortcuts import render,redirect
from django.http import JsonResponse
from ..login.models import *

# Create your views here.

def home(request):
    if request.COOKIES.get('user') != "" and request.COOKIES.get('user') != None:
        usuario = Usuarios.objects.filter(
            email=request.COOKIES.get('user')
        ).first()
        empresa = EmpresasUsuario.objects.filter(usuario=usuario)
        if not empresa:
            empresa_vacia = True
        else:
            empresa_vacia = False
        return render(request, "home.html", {'usuario': usuario,'empresa_vacia':empresa_vacia})
    else:
        return redirect('login')