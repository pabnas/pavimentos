from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..login.models import *


def abonos_home(request):
    if request.COOKIES.get('user') != "" and request.COOKIES.get('user') != None:
        empresa, usuario = buscar_empresa(request)
        clientes = Clientes.objects.filter(empresa=empresa)
        return render(request, "abonos.html",
                      {'usuario': usuario, 'empresa': empresa, 'clientes': clientes}
                     )
    else:
        return redirect('login')

def buscar_empresa(request):
    usuario = Usuarios.objects.only('email').get(
        email=request.COOKIES.get('user')
    )
    empresa_rel = EmpresasUsuario.objects.filter(usuario=usuario).first()
    return empresa_rel.empresa, usuario