from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.shortcuts import redirect
from collections import namedtuple
from django.core.serializers.json import DjangoJSONEncoder
import json
import sys
from datetime import datetime as dt
from django.contrib.auth import authenticate, login
from .models import *

#https://docs.djangoproject.com/en/2.1/topics/db/sql/

def index(request):
    return render(request,"login.html",{})

def registro(request):
    return render(request,"registro.html",{})

def validar_registro(request):
    data = dict()
    try:
        empresa_rel = buscar_empresa(request)

        if request.POST['password'] == "":
            raise Exception("Contraseña vacia")
        if request.POST['nombre'] == "":
            raise Exception("Nombre vacio")

        usuarios_doc = Usuarios.objects.filter(
            document_reference=request.POST["numero_doc"],
            document_type=request.POST["tipo"]
        ).first()

        usuarios_correo = Usuarios.objects.filter(
            email=request.POST["correo"]
        ).first()

        if(usuarios_doc != None):
            resultado = "Ya se tiene registrado el documento"
        elif(usuarios_correo != None):
            resultado = "Ya se tiene registrado el correo"
        else:
            rol = Roles.objects.filter(nombre="vendedor").first()

            usuario_nuevo = Usuarios.objects.create(
                nombre = request.POST["nombre"],
                apellido = request.POST["apellido"],
                telefono = request.POST["telefono"],
                email = request.POST["correo"],
                contraseña = request.POST["password"],
                document_type = request.POST["tipo"],
                document_reference = request.POST["numero_doc"],
                created_at = dt.now(),
                rol=rol,
            )
            ##agregar relacion
            EmpresasUsuario.objects.create(
                empresa = empresa_rel,
                usuario = usuario_nuevo,
            )

            resultado = "Se ha creado el Usuario"
            data["url"] = "/registro"
    except Exception as e:
        resultado = str(e)
    data["result"] = resultado
    return JsonResponse(data)

def validar_login(request):
    data = dict()
    data["url"] = "/"
    data["msg"] = ""
    try:
        usuario = Usuarios.objects.filter(
            email=request.POST["correo"],
            contraseña=request.POST['password']
        ).first()

        if usuario != None:
            data["url"] = "home"
        else:
            data["msg"] = "Las credenciales son incorrectas"
    except Exception as e:
        data["msg"] = str(e)
    return JsonResponse(data)

def buscar_empresa(request):
    usuario = Usuarios.objects.only('email').get(
        email=request.COOKIES.get('user')
    )
    empresa_rel = EmpresasUsuario.objects.filter(usuario=usuario).first()
    return empresa_rel.empresa