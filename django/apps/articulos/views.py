from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render,redirect
from ..login.models import *
from django.core.files.storage import FileSystemStorage
from datetime import datetime as dt

def articulos_principal(request):
    if request.COOKIES.get('user') != "" and request.COOKIES.get('user') != None:
        usuario = Usuarios.objects.filter(
            email=request.COOKIES.get('user')
        ).first()
        articulos = Productos.objects.filter(empresa = buscar_empresa(request)).order_by('codigo')
        proveedores = Proveedores.objects.filter(empresa_0 = buscar_empresa(request))
        return render(request, "articulos.html", {'usuario': usuario,'articulos': articulos,'proveedores':proveedores})
    else:
        return redirect('login')

def nuevo(request):
    data = dict()
    data["success"] = ""
    try:
        #verificacion de codigo unico
        producto_val = Productos.objects.filter(codigo=request.POST["Codigo"], empresa = buscar_empresa(request)).first()
        if(producto_val != None):
            raise NameError('Producto ya existente')
        #verficacion de tipo de imagen

        try:
            imagen = request.FILES["Imagen"]
            if(imagen.content_type != 'image/jpg' and
                    imagen.content_type != 'image/png' and imagen.content_type != 'image/jpeg'):
                raise NameError('Formato de archivo ' + imagen.content_type + ' no valido')
            #cargar a DB
            fs = FileSystemStorage()
            fs_name = fs.get_available_name(imagen.name, max_length=None)
            file_name = fs.save(fs_name, imagen)
            url = fs.url(file_name)
        except:
            url = ""

        dt.now()
        empresa = buscar_empresa(request)

        proveedor = Proveedores.objects.only('id').get(id=request.POST["Proveedor"],empresa_0 = buscar_empresa(request))
        producto = Productos.objects.create(
            marca=request.POST["Marca"],
            nombre=request.POST["Articulo"],
            codigo=request.POST["Codigo"],
            costo=float(request.POST["Costo"]),
            categoria=request.POST["Categoria"],
            porcentaje=float(request.POST["Impuesto"]),
            valor_unitario= float(request.POST["Valor_unitario"]),
            imagen_url= url,
            proveedor=proveedor,
            empresa=empresa,
        )

        ##se inicializa el inventario en 0
        Inventario.objects.create(
            cantidad_producto=0,
            producto=producto,
            created_at=dt.now()
        )

        resultado = "Se ha creado el artículo"
        data["success"] = "true"
    except Exception as e:
        resultado = str(e)
    data["result"] = resultado
    return JsonResponse(data)

def editar(request):
    data = dict()
    data["success"] = ""
    try:
        producto = Productos.objects.filter(
            codigo=request.POST["Codigo"],empresa = buscar_empresa(request)
        ).first()
        proveedor = Proveedores.objects.get(id=request.POST["Proveedor"],empresa_0 = buscar_empresa(request))

        if producto == None:
            raise NameError("El producto con el codigo " + request.POST["Codigo"] + " no existe")

        #si se subio un archivo
        if(request.FILES):
            imagen = request.FILES["Imagen"]
            if (imagen.content_type != 'image/jpg' and
                    imagen.content_type != 'image/png' and imagen.content_type != 'image/jpeg'):
                raise NameError('Formato de archivo ' + imagen.content_type + ' no valido')
            fs = FileSystemStorage()
            img_old = producto.imagen_url
            img_old = img_old.replace(settings.MEDIA_URL,"")
            fs.delete(img_old)
            fs_name = fs.get_available_name(imagen.name, max_length=None)
            file_name = fs.save(fs_name, imagen)
            url = fs.url(file_name)
        else:
            url = producto.imagen_url

        producto.marca=request.POST["Marca"]
        producto.nombre=request.POST["Articulo"]
        producto.valor_unitario=float(request.POST["Valor_unitario"])
        producto.categoria=request.POST["Categoria"]
        producto.proveedor=proveedor
        producto.porcentaje=float(request.POST["Impuesto"])
        producto.costo=float(request.POST["Costo"])
        producto.imagen_url=url
        producto.save()

        resultado = "Se ha modificado el artículo"
        data["success"] = "true"
    except Exception as e:
        resultado = str(e)
    data["result"] = resultado
    return JsonResponse(data)

def borrar(request):
    data = dict()
    data["success"] = ""
    try:
        producto = Productos.objects.filter(
            id=request.POST["ID"],
        ).first()
        codigo = producto.codigo

        fs = FileSystemStorage()
        img_old = producto.imagen_url
        img_old = img_old.replace(settings.MEDIA_URL,"")
        fs.delete(img_old)

        producto.delete()
        resultado = "Se ha eliminado el artículo con el codigo: " + codigo
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

def consultar(request):
    data = dict()
    data["success"] = ""
    try:
        producto = Productos.objects.filter(
            codigo=request.GET["Codigo"],empresa = buscar_empresa(request)
        ).first()

        if producto == None:
            raise NameError("El producto con el codigo " + request.POST["Codigo"] + " no existe")

        resultado = "Se ha consultado el artículo: " + producto.codigo
        data["success"] = "true"
        data["data_articulo"] = [producto.id,producto.codigo,producto.nombre,producto.marca,producto.categoria,producto.valor_unitario,producto.porcentaje]
    except Exception as e:
        resultado = str(e)
    data["result"] = resultado
    return JsonResponse(data)