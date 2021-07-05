from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..login.models import *
from datetime import datetime as dt
from django.forms.models import model_to_dict
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from ..email import *

import base64
from django.core.files.base import ContentFile

def ventas_principal(request):
    if request.COOKIES.get('user') != "" and request.COOKIES.get('user') != None:
        empresa , usuario = buscar_empresa(request)
        clientes = Clientes.objects.filter(empresa = empresa)
        ciudades = Ciudad.objects.all()
        productos = Productos.objects.filter(empresa = empresa)

        ventas = Ventas.objects.filter(finalizada=False, usuario=usuario)

        return render(request, "ventas.html",
                      {'usuario': usuario, 'clientes': clientes, 'ventas': ventas, 'ciudades': ciudades, 'productos':productos}
                     )
    else:
        return redirect('login')

def id_venta_nueva(request):
    data = dict()
    data["success"] = ""
    try:
        empresa, usuario = buscar_empresa(request)
        cliente = Clientes.objects.filter(empresa=empresa , id= request.GET["Cliente_id"]).first()

        venta = Ventas.objects.create(
            created_at = dt.now(),
            usuario = usuario,
            cliente = cliente,
            finalizada = False
        )

        data["ID"] = venta.id
        data["Cliente"] = model_to_dict(cliente)
        data["fecha"] = dt.now().strftime("%Y-%m-%d %H:%M:%S")
        resultado = "Se ha creado la venta con el ID: " + str(venta.id)
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
        venta = Ventas.objects.filter(usuario=usuario,id=request.POST["id_venta"]).first()

        articulos = CarritoVentas.objects.create(
            ventas=venta,
            producto = producto,
            cantidad = request.POST["Cantidad"],
            descuento = float(request.POST["Descuento"]),
            comentario = request.POST["Comentario"],
        )

        codigo = producto.codigo
        resultado = "Se ha agregado el artículo con el codigo: " + codigo
        data["ID_Venta"] = venta.id
        data["success"] = "true"
    except Exception as e:
        resultado = str(e)
    data["result"] = resultado
    return JsonResponse(data)

def cargar_venta(request):
    try:
        empresa, usuario = buscar_empresa(request)

        productos = Productos.objects.filter(empresa=empresa)
        venta = Ventas.objects.filter(usuario=usuario, id=request.GET["id_venta"]).first()
        articulos = CarritoVentas.objects.filter(ventas=venta).order_by('producto__codigo')

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

        return render(request, "ventas_tabla.html",
                      {"Venta" : venta,"Articulos":articulos_list,'productos': productos,"empresa":empresa})
    except Exception as e:
        data = dict()
        data["result"] = e
        return JsonResponse(data)

def cancelar_venta(request):
    data = dict()
    data["success"] = ""
    try:
        empresa, usuario = buscar_empresa(request)
        venta = Ventas.objects.filter(id=request.POST["ID_venta"],usuario=usuario).first()
        carro_venta = CarritoVentas.objects.filter(ventas=venta)

        carro_venta.delete()
        venta.delete()
        resultado = "Se ha eliminado la venta con el id: " + request.POST["ID_venta"]
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
        venta = Ventas.objects.filter(id=request.POST["ID_venta"],usuario=usuario).first()
        articulos = CarritoVentas.objects.filter(ventas=venta)

        ##se guarda la captura
        imagen = request.POST["Image"]
        format, imgstr = imagen.split(';base64,')
        ext = format.split('/')[-1]
        imagen = ContentFile(base64.b64decode(imgstr), name='Factura_' + request.POST["ID_venta"] + '.' + ext)

        fs = FileSystemStorage()
        fs_name = fs.get_available_name(imagen.name, max_length=None)
        file_name = fs.save(fs_name, imagen)
        url = fs.url(file_name)

        ##se envia la imagen al correo del cliente
        ruta_imagen= settings.MEDIA_ROOT + "/" +fs_name
        img_to_pdf(ruta_imagen)
        Enviar_correo("Factura","Se adjunta la factura de la venta",[venta.cliente.email],"file.pdf")

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

        ##se verifica si se tiene la cantidad de productos si no se arroja un error
        for articulo in articulos_list:
            producto = Productos.objects.filter(codigo=articulo["Codigo"]).first()
            inventario = Inventario.objects.filter(producto=producto).first()
            if articulo["Cantidad"] > inventario.cantidad_producto:
                raise NameError('Se tiene ' + str(inventario.cantidad_producto) + ' producto(s) con el codigo '
                                + producto.codigo + ' en el inventario y se estan vendiendo ' + str(articulo["Cantidad"])
                                + ', porfavor contacte al proveedor del articulo')
            else:
                inventario.cantidad_producto -= articulo["Cantidad"]

        ##se descuenta la cantidad de inventario
        for articulo in articulos_list:
            producto = Productos.objects.filter(codigo=articulo["Codigo"]).first()
            inventario = Inventario.objects.filter(producto=producto).first()
            inventario.cantidad_producto -= articulo["Cantidad"]
            inventario.save()

        venta.subtotal =  float(request.POST["Subtotal"])
        venta.descuento = float(request.POST["Descuento"])
        venta.iva = float(request.POST["IVA"])
        venta.total = float(request.POST["Total"])
        venta.finalizada = True
        venta.save()

        ##se guarda la informacion en la tabla factura
        try:
            voucher = request.POST["Num_voucher"]
        except Exception as e:
            voucher = "no se tiene"

        factura = Factura.objects.create(
            numero_factura = request.POST["ID_venta"],
            created_at = dt.now(),
            ventas = venta,
            subtotal = float(request.POST["Subtotal"]),
            descuento = float(request.POST["Descuento"]),
            iva = float(request.POST["IVA"]),
            total = float(request.POST["Total"]),
            link_detalles = url,
            metodo_de_pago = request.POST["Forma_de_pago"],
            numero_de_vouche = voucher,
        )

        ##se guarda el movimiento en el log
        for articulo in articulos_list:
            producto = Productos.objects.filter(codigo=articulo["Codigo"]).first()
            InventarioLog.objects.create(
                producto = producto,
                usuario = usuario,
                fecha = dt.now().strftime("%Y-%m-%d %H:%M:%S"),
                comentario = "Se vendieron " + str(articulo["Cantidad"]) + " articulos con el ID "
                ##TODO: terminar codigo del log
            )

        resultado = "Se ha finalizado la venta con el id: " + request.POST["ID_venta"]
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

