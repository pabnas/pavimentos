from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..login.models import *

def inventario_principal(request):
    if request.COOKIES.get('user') != "" and request.COOKIES.get('user') != None:
        empresa , usuario = buscar_empresa(request)
        productos = Productos.objects.filter(empresa=empresa)
        inventarios = Inventario.objects.filter(producto__in=productos.values_list('id', flat=True))

        inventario_list = []
        ## agrega los articulos a la lista
        for inventario in inventarios:
            temp = {
                "Codigo": inventario.producto.codigo,
                "Nombre": inventario.producto.nombre,
                "Cantidad": inventario.cantidad_producto,
                "Created_at": inventario.created_at,
                "Modify_at": inventario.modify_at,
                "Finished_at": inventario.finished_at
            }
            inventario_list.append(temp)

        return render(request, "inventario.html",
                      {'usuario': usuario, 'empresa': empresa, 'productos':productos,'inventarios':inventario_list}
                     )
    else:
        return redirect('login')

def buscar_empresa(request):
    usuario = Usuarios.objects.only('email').get(
        email=request.COOKIES.get('user')
    )
    empresa_rel = EmpresasUsuario.objects.filter(usuario=usuario).first()
    return empresa_rel.empresa , usuario