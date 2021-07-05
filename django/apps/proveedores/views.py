from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..login.models import *

def proveedores_principal(request):
    if request.COOKIES.get('user') != "" and request.COOKIES.get('user') != None:
        usuario = Usuarios.objects.filter(
            email=request.COOKIES.get('user')
        ).first()

        proveedores = Proveedores.objects.filter(empresa_0 = buscar_empresa(request))

        return render(request,"proveedores.html",{'usuario': usuario,'proveedores': proveedores}
        )
    else:
        return redirect('login')


def nuevo(request):
    data = dict()
    data["success"] = ""
    try:
        empresa = buscar_empresa(request)
        Proveedores.objects.create(
            nombre=request.POST["Nombre"],
            apellido=request.POST["Apellido"],
            empresa=request.POST["Empresa"],
            telefono=request.POST["Telefono"],
            email=request.POST["Email"],
            document_type=request.POST["Tipo_doc"],
            document_id=request.POST["Documento"],
            empresa_0 = empresa,
        )
        resultado = "Se ha creado el proveedor"
        data["success"] = "true"
    except Exception as e:
        resultado = str(e)
    data["result"] = resultado
    return JsonResponse(data)

def editar(request):
    data = dict()
    data["success"] = ""
    try:
        proveedor = Proveedores.objects.get(id=request.POST["Id_form"],empresa_0 = buscar_empresa(request))

        proveedor.nombre=request.POST["Nombre"]
        proveedor.apellido=request.POST["Apellido"]
        proveedor.telefono=request.POST["Telefono"]
        proveedor.email=request.POST["Email"]
        proveedor.empresa=request.POST["Empresa"]
        proveedor.document_type=request.POST["Tipo_doc"]
        proveedor.document_id=request.POST["Documento"]
        proveedor.save()

        resultado = "Se ha modificado el proveedor"
        data["success"] = "true"
    except Exception as e:
        resultado = str(e)
    data["result"] = resultado
    return JsonResponse(data)

def borrar(request):
    data = dict()
    data["success"] = ""
    try:
        proveedor = Proveedores.objects.filter(
            id=request.POST["ID"],empresa_0 = buscar_empresa(request)
        ).first()

        nombre = proveedor.nombre + " " + proveedor.apellido
        proveedor.delete()
        resultado = "Se ha eliminado el proveedor: " + nombre
        data["success"] = "true"
    except Exception as e:
        resultado = str(e)
    data["result"] = resultado
    return JsonResponse(data)

def buscar_empresa(request):
    usuario = Usuarios.objects.only('email').get(
        email=request.COOKIES.get('user')
    )
    empresa_rel = EmpresasUsuario.objects.filter(usuario=usuario).first()
    return empresa_rel.empresa