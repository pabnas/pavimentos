from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..login.models import *
from datetime import datetime as dt
from django.forms.models import model_to_dict
from django.core.files.storage import FileSystemStorage

import base64
from django.core.files.base import ContentFile

def compras_principal(request):
    if request.COOKIES.get('user') != "" and request.COOKIES.get('user') != None:
        empresa , usuario = buscar_empresa(request)
        proveedores = Proveedores.objects.filter(empresa_0 = empresa)
        compras = Compras.objects.filter(finalizada=False, usuario=usuario)

        return render(request, "compras.html",
                      {'usuario': usuario, 'proveedores': proveedores, 'compras': compras}
                     )
    else:
        return redirect('login')

def id_compra_nueva(request):
    data = dict()
    data["success"] = ""
    try:
        empresa, usuario = buscar_empresa(request)
        proveedor = Proveedores.objects.filter(empresa_0=empresa,id=request.GET["Proveedor_id"]).first()

        compra = Compras.objects.create(
            created_at = dt.now(),
            usuario = usuario,
            proveedor = proveedor,
            finalizada = False
        )

        data["ID"] = compra.id
        resultado = "Se ha creado la compra con el ID: " + str(compra.id)
        data["success"] = "true"
    except Exception as e:
        resultado = str(e)
    data["result"] = resultado
    return JsonResponse(data)

def cargar_detalles(request):
    data = dict()
    data["success"] = ""
    try:
        empresa , usuario = buscar_empresa(request)
        producto = Productos.objects.filter(
            codigo=request.GET["id_producto"], empresa=empresa
        ).first()

        data["valor"] = producto.valor_unitario
        codigo = producto.codigo
        resultado = "Se ha consultado el artículo con el codigo: " + codigo
        data["success"] = "true"
    except Exception as e:
        resultado = str(e)
    data["result"] = resultado
    return JsonResponse(data)

def agregar_articulo(request):
    data = dict()
    data["success"] = ""
    try:
        empresa, usuario = buscar_empresa(request)

        producto = Productos.objects.filter(codigo=request.POST["Codigo"], empresa=empresa).first()
        compra = Compras.objects.filter(usuario=usuario,id=request.POST["id_compra"]).first()

        articulos = CarritoCompras.objects.create(
            compras=compra,
            producto = producto,
            cantidad = request.POST["Cantidad"],
            descuento = float(request.POST["Descuento"]),
            comentario = request.POST["Comentario"],
        )

        codigo = producto.codigo
        resultado = "Se ha agregado el artículo con el codigo: " + codigo
        data["ID_compra"] = compra.id
        data["success"] = "true"
    except Exception as e:
        resultado = str(e)
    data["result"] = resultado
    return JsonResponse(data)

def cargar_compra(request):
    try:
        empresa, usuario = buscar_empresa(request)

        productos = Productos.objects.filter(empresa=empresa)
        compra = Compras.objects.filter(usuario=usuario, id=request.GET["id_compra"]).first()
        articulos = CarritoCompras.objects.filter(compras=compra).order_by('producto__codigo')

        articulos_list = []
        ## agrega los articulos a la lista
        for articulo in articulos:
            valor = float(articulo.producto.valor_unitario) * float(articulo.cantidad)
            descuento = (float(articulo.descuento)/100)*valor
            valor = valor - descuento
            total = valor
    
            temp = {
                "ID" : articulo.producto.id,
                "Codigo": articulo.producto.codigo,
                "Nombre" : articulo.producto.nombre,
                "Valor_Unidad" : articulo.producto.valor_unitario,
                "Unidades" : articulo.cantidad,
                "Descuento": descuento,
                "Valor" :  total,
                "Comentario": articulo.comentario,
            }
            articulos_list.append(temp)

        return render(request, "compras_tabla.html",{"Compra" : compra,"Articulos":articulos_list,'productos': productos})
    except Exception as e:
        data = dict()
        data["result"] = e
        return JsonResponse(data)

def cancelar_compra(request):
    data = dict()
    data["success"] = ""
    try:
        empresa, usuario = buscar_empresa(request)
        carro = Compras.objects.filter(id=request.POST["ID_compra"],usuario=usuario).first()
        carro_producto = CarritoCompras.objects.filter(compras=carro)

        carro_producto.delete()
        carro.delete()
        resultado = "Se ha eliminado la compra con el id: " + request.POST["ID_compra"]
        data["success"] = "true"
    except Exception as e:
        resultado = str(e)
    data["result"] = resultado
    return JsonResponse(data)

def finalizar(request):
    data = dict()
    data["success"] = ""
    try:
        empresa, usuario = buscar_empresa(request)
        carro = Compras.objects.filter(id=request.POST["ID_compra"],usuario=usuario).first()
        articulos = CarritoCompras.objects.filter(compras=carro)

        ##se cuenta cuantos articulos en total hay y se dejan en una sola lista
        articulos_list = []
        for articulo in articulos:
            repetido = next((i for i, item in enumerate(articulos_list) if item["Codigo"] == articulo.producto.codigo), None)
            if repetido == None:
                temp = {
                    "Codigo": articulo.producto.codigo,
                    "Cantidad": articulo.cantidad,
                }
                articulos_list.append(temp)
            else:
                articulos_list[repetido]["Cantidad"] += articulo.cantidad

        ##se suma la cantidad al inventario
        for articulo in articulos_list:
            producto = Productos.objects.filter(codigo=articulo["Codigo"]).first()
            inventario = Inventario.objects.filter(producto=producto).first()
            inventario.cantidad_producto += articulo["Cantidad"]
            inventario.save()

        ##se guarda el movimiento en el log
        for articulo in articulos_list:
            producto = Productos.objects.filter(codigo=articulo["Codigo"]).first()
            InventarioLog.objects.create(
                producto=producto,
                usuario=usuario,
                fecha=dt.now().strftime("%Y-%m-%d %H:%M:%S"),
                comentario="Se compraron " + str(articulo["Cantidad"]) + " articulos con el ID "
                ##TODO: terminar codigo del log
            )

        carro.subtotal =  float(request.POST["Subtotal"])
        carro.descuento = float(request.POST["Descuento"])
        carro.iva = float(request.POST["IVA"])
        carro.total = float(request.POST["Total"])
        carro.finalizada = True
        carro.save()

        ##se guarda la captura
        imagen = request.POST["Image"]
        format, imgstr = imagen.split(';base64,')
        ext = format.split('/')[-1]
        imagen = ContentFile(base64.b64decode(imgstr), name='Factura_' + request.POST["ID_compra"]+'.'+ ext)

        fs = FileSystemStorage()
        fs_name = fs.get_available_name(imagen.name, max_length=None)
        file_name = fs.save(fs_name, imagen)
        url = fs.url(file_name)

        resultado = "Se ha finalizado la compra con el id: " + request.POST["ID_compra"]
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

