from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..login.models import *
from django.core.files.storage import FileSystemStorage
from django.conf import settings

def empresas_principal(request):
    if request.COOKIES.get('user') != "" and request.COOKIES.get('user') != None:
        usuario = Usuarios.objects.only('email').get(
            email=request.COOKIES.get('user')
        )

        empresa_rel = EmpresasUsuario.objects.filter(usuario = usuario).first()
        empresa = empresa_rel.empresa
        roles = Roles.objects.all()

        lista_usuarios = EmpresasUsuario.objects.filter(empresa= empresa)
        return render(request, "empresas.html",
                      {'usuario': usuario, 'empresa': empresa , 'lista_usuarios':lista_usuarios,'roles':roles}
                     )
    else:
        return redirect('login')

def agregar(request):
    data = dict()
    data["success"] = ""
    try:
        empresa , usuario = buscar_empresa(request)

        usuario_nuevo = Usuarios.objects.filter(email=request.POST["Correo"]).first()
        if not usuario_nuevo:
            raise ValueError("No se encuentra el usuario")

        relacion = EmpresasUsuario.objects.filter(usuario=usuario_nuevo)
        if relacion:
            raise ValueError("Ya se tiene agregado el usuario")

        EmpresasUsuario.objects.create(
            empresa=empresa,
            usuario=usuario_nuevo,
        )

        resultado = "Se ha agregado el Usuario"
        data["success"] = "true"
    except Exception as e:
        resultado = str(e)
    data["result"] = resultado
    return JsonResponse(data)

def editar_empresa(request):
    data = dict()
    data["success"] = ""
    try:
        empresa , usuario = buscar_empresa(request)

        # si se subio un archivo
        if (request.FILES):
            imagen = request.FILES["Imagen"]
            if (imagen.content_type != 'image/jpg' and
                    imagen.content_type != 'image/png' and imagen.content_type != 'image/jpeg'):
                raise NameError('Formato de archivo ' + imagen.content_type + ' no valido')
            fs = FileSystemStorage()
            img_old = empresa.ruta_logo
            img_old = img_old.replace(settings.MEDIA_URL, "")
            fs.delete(img_old)
            fs_name = fs.get_available_name(imagen.name, max_length=None)
            file_name = fs.save(fs_name, imagen)
            url = fs.url(file_name)
        else:
            url = empresa.ruta_logo

        empresa.nombre = request.POST["Nombre"]
        empresa.telefono = request.POST["Telefono"]
        empresa.email = request.POST["Correo"]
        empresa.rl_nombre = request.POST["Nombre_rl"]
        empresa.rl_cedula = request.POST["Cedula_rl"]
        empresa.rl_telefono = request.POST["Telefono_rl"]
        empresa.ruta_logo = url
        empresa.save()
        resultado = "Se han guardado los cambios"
        data["success"] = "true"
    except Exception as e:
        resultado = str(e)
    data["result"] = resultado
    return JsonResponse(data)

def editar_miembro(request):
    data = dict()
    data["success"] = ""
    try:
        empresa , usuario = buscar_empresa(request)
        usuario_modificar = Usuarios.objects.filter(id=request.POST["Id_usuario"]).first()
        rol = Roles.objects.filter(id=request.POST["Rol"]).first()
        usuario_modificar.rol = rol
        usuario_modificar.save()

        resultado = "Se han guardado los cambios"
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