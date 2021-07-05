from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..login.models import *
from ..funciones_generales import *


def orden_home(request):
    if request.COOKIES.get('user') != "" and request.COOKIES.get('user') != None:
        empresa, usuario = buscar_empresa(request)
        clientes = Clientes.objects.filter(empresa=empresa)
        return render(request, "orden_de_compra.html",
                      {'usuario': usuario, 'empresa': empresa, 'clientes': clientes}
                     )
    else:
        return redirect('login')

