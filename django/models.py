# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class CarritoCompras(models.Model):
    compras = models.ForeignKey('Compras', models.DO_NOTHING, blank=True, null=True)
    producto = models.ForeignKey('Productos', models.DO_NOTHING, blank=True, null=True)
    cantidad = models.IntegerField(blank=True, null=True)
    descuento = models.FloatField(blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'carrito_compras'


class CarritoVentas(models.Model):
    ventas = models.ForeignKey('Ventas', models.DO_NOTHING, blank=True, null=True)
    producto = models.ForeignKey('Productos', models.DO_NOTHING, blank=True, null=True)
    cantidad = models.IntegerField(blank=True, null=True)
    descuento = models.FloatField(blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'carrito_ventas'


class Ciudad(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)
    pais = models.ForeignKey('Pais', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ciudad'


class Clientes(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)
    apellido = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=10, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    ciudad = models.ForeignKey(Ciudad, models.DO_NOTHING, blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)
    empresa = models.ForeignKey('Empresas', models.DO_NOTHING, blank=True, null=True)
    document_type = models.CharField(max_length=255, blank=True, null=True)
    document_number = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clientes'


class Compras(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    iva = models.FloatField(blank=True, null=True)
    subtotal = models.FloatField(blank=True, null=True)
    descuento = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, blank=True, null=True)
    proveedor = models.ForeignKey('Proveedores', models.DO_NOTHING, blank=True, null=True)
    finalizada = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'compras'


class Empresas(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    ciudad = models.ForeignKey(Ciudad, models.DO_NOTHING, blank=True, null=True)
    telefono = models.CharField(max_length=10, blank=True, null=True)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    ruta_logo = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=6, blank=True, null=True)
    rl_nombre = models.CharField(max_length=255, blank=True, null=True)
    rl_cedula = models.CharField(max_length=20, blank=True, null=True)
    rl_telefono = models.CharField(max_length=30, blank=True, null=True)
    nit = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'empresas'


class EmpresasUsuario(models.Model):
    empresa = models.ForeignKey(Empresas, models.DO_NOTHING)
    usuario = models.ForeignKey('Usuarios', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'empresas_usuario'


class Estado(models.Model):
    estado_factura = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'estado'


class Factura(models.Model):
    numero_factura = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    ventas = models.ForeignKey('Ventas', models.DO_NOTHING, blank=True, null=True)
    iva = models.FloatField(blank=True, null=True)
    subtotal = models.IntegerField(blank=True, null=True)
    descuento = models.FloatField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    metodo_de_pago = models.TextField(blank=True, null=True)
    numero_de_vouche = models.TextField(blank=True, null=True)
    link_detalles = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'factura'


class Inventario(models.Model):
    cantidad_producto = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    producto = models.ForeignKey('Productos', models.DO_NOTHING, blank=True, null=True)
    modify_at = models.DateTimeField(blank=True, null=True)
    finished_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inventario'


class InventarioLog(models.Model):
    producto = models.ForeignKey('Productos', models.DO_NOTHING, blank=True, null=True)
    usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inventario_log'


class Pais(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pais'


class Productos(models.Model):
    marca = models.CharField(max_length=255, blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    codigo = models.CharField(unique=True, max_length=255, blank=True, null=True)
    valor_unitario = models.FloatField(blank=True, null=True)
    categoria = models.CharField(max_length=255, blank=True, null=True)
    porcentaje = models.FloatField(blank=True, null=True)
    imagen_url = models.CharField(max_length=255, blank=True, null=True)
    proveedor = models.ForeignKey('Proveedores', models.DO_NOTHING, blank=True, null=True)
    costo = models.FloatField(blank=True, null=True)
    empresa = models.ForeignKey(Empresas, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'productos'


class Proveedores(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)
    apellido = models.CharField(max_length=255, blank=True, null=True)
    empresa = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=10, blank=True, null=True)
    empresa_0 = models.ForeignKey(Empresas, models.DO_NOTHING, db_column='empresa_id', blank=True, null=True)  # Field renamed because of name conflict.
    document_type = models.CharField(max_length=255, blank=True, null=True)
    document_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'proveedores'


class Roles(models.Model):
    nombre = models.CharField(max_length=30, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles'


class Sede(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=10, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    pais_id = models.IntegerField(blank=True, null=True)
    ciudad_id = models.IntegerField(blank=True, null=True)
    empresa = models.ForeignKey(Empresas, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sede'


class Usuarios(models.Model):
    nombre = models.CharField(max_length=255, blank=True, null=True)
    apellido = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=10, blank=True, null=True)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    contraseña = models.CharField(max_length=255, blank=True, null=True)
    document_type = models.CharField(max_length=255, blank=True, null=True)
    document_reference = models.CharField(max_length=255, blank=True, null=True)
    accepted_service_terms = models.TextField(blank=True, null=True)  # This field type is a guess.
    accepted_privacy_policy = models.TextField(blank=True, null=True)  # This field type is a guess.
    created_at = models.DateTimeField(blank=True, null=True)
    rol = models.ForeignKey(Roles, models.DO_NOTHING, db_column='rol', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuarios'


class Ventas(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    iva = models.FloatField(blank=True, null=True)
    subtotal = models.FloatField(blank=True, null=True)
    descuento = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    usuario = models.ForeignKey(Usuarios, models.DO_NOTHING, blank=True, null=True)
    cliente = models.ForeignKey(Clientes, models.DO_NOTHING, blank=True, null=True)
    finalizada = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ventas'
