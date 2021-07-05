from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..login.models import *

def facturas_principal(request):
    if request.COOKIES.get('user') != "" and request.COOKIES.get('user') != None:
        empresa, usuario = buscar_empresa(request)
        clientes = Clientes.objects.filter(empresa=empresa)
        return render(request, "factura.html",
                      {'usuario': usuario, 'empresa': empresa, 'clientes': clientes}
                     )
    else:
        return redirect('login')

def consultar(request):
    try:
        if request.GET['Cliente'] == "":
            raise Exception("Campo Cliente vacio")

        empresa, usuario = buscar_empresa(request)
        tipo, numero = request.GET['Cliente'].split()
        cliente = Clientes.objects.filter(document_type=tipo,document_number=numero,empresa=empresa).first()
        ventas = Ventas.objects.filter(cliente=cliente, finalizada=True)
        facturas = Factura.objects.filter(ventas__in=ventas.values_list('id', flat=True))
        resultado = "Se han encontrado " + str(facturas.count()) + " Factura(s)"

        facturas_list = []
        ## agrega los articulos a la lista
        for factura in facturas:
            temp = {
                "ID": factura.ventas.id,
                "Fecha": factura.created_at,
                "Total": factura.total,
                "Medio_de_Pago": factura.metodo_de_pago,
                "Vendedor": factura.ventas.usuario.nombre + " " + factura.ventas.usuario.apellido,
                "Detalles": factura.link_detalles,
            }
            facturas_list.append(temp)

        return render(request, "factura_tabla.html",{"Facturas": facturas_list})
    except Exception as e:
        data = dict()
        data["result"] = e
        return JsonResponse(data)


def buscar_empresa(request):
    usuario = Usuarios.objects.only('email').get(
        email=request.COOKIES.get('user')
    )
    empresa_rel = EmpresasUsuario.objects.filter(usuario=usuario).first()
    return empresa_rel.empresa , usuario