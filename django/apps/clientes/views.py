from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..login.models import *

def clientes_principal(request):
    if request.COOKIES.get('user') != "" and request.COOKIES.get('user') != None:
        empresa , usuario = buscar_empresa(request)
        ciudades = Ciudad.objects.all()
        clientes = Clientes.objects.filter(empresa = empresa)
        return render(
            request,
            "clientes.html",
            {'ciudades': ciudades,
             'clientes': clientes,
             'usuario': usuario
             }
        )
    else:
        return redirect('login')

def nuevo(request):
    data = dict()
    data["success"] = ""
    try:
        empresa , usuario = buscar_empresa(request)

        ciudad = Ciudad.objects.only('id').get(id=request.POST["Ciudad"])

        Clientes.objects.create(
            nombre=request.POST["Nombre"],
            apellido=request.POST["Apellido"],
            telefono=request.POST["Telefono"],
            email=request.POST["Email"],
            direccion=request.POST["Direccion"],
            ciudad=ciudad,
            comentario=request.POST["Comentario"],
            document_type=request.POST["Tipo_doc"],
            document_number=request.POST["Documento"],
            empresa=empresa
        )
        resultado = "Se ha creado el Cliente"
        data["success"] = "true"
    except Exception as e:
        resultado = str(e)
    data["result"] = resultado
    return JsonResponse(data)

def editar(request):
    data = dict()
    data["success"] = ""
    try:
        cliente = Clientes.objects.get(id=request.POST["ID"])
        ciudad = Ciudad.objects.only('id').get(id=request.POST["Ciudad"])

        cliente.nombre=request.POST["Nombre"]
        cliente.apellido=request.POST["Apellido"]
        cliente.telefono=request.POST["Telefono"]
        cliente.email=request.POST["Email"]
        cliente.direccion=request.POST["Direccion"]
        cliente.ciudad=ciudad
        try:
            cliente.comentario=request.POST["Comentario"]
        except:
            pass
        cliente.document_type = request.POST["Tipo_doc"]
        cliente.document_number = request.POST["Documento"]
        cliente.save()

        resultado = "Se ha modificado el cliente"
        data["success"] = "true"
    except Exception as e:
        resultado = str(e)
    data["result"] = resultado
    return JsonResponse(data)

def borrar(request):
    data = dict()
    data["success"] = ""
    try:
        cliente = Clientes.objects.filter(
            id=request.POST["ID"],
        ).first()

        nombre = cliente.nombre + " " + cliente.apellido
        cliente.delete()
        resultado = "Se ha eliminado el cliente: " + nombre
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
    return empresa_rel.empresa , usuario

def consultar(request):
    data = dict()
    data["success"] = ""
    try:
        cliente = Clientes.objects.filter(
            document_type=request.GET["Tipo_documento"],
            document_number=request.GET["Numero_documento"],
        ).first()

        resultado = "Se ha consultado el cliente: " + cliente.nombre + " " + cliente.apellido
        data["success"] = "true"
        data["datos_cliente"] = [cliente.id,cliente.nombre,cliente.apellido,cliente.telefono,cliente.email,cliente.document_type,cliente.document_number,cliente.direccion,cliente.ciudad.id]
    except Exception as e:
        resultado = str(e)
    data["result"] = resultado
    return JsonResponse(data)