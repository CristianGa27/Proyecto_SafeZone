# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Configuracionsistema(models.Model):
    clave = models.CharField(unique=True, max_length=100)
    valor = models.TextField()
    descripcion = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=7, blank=True, null=True)
    fecha_actualizacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'configuracionsistema'


class Historialreporte(models.Model):
    reporte = models.ForeignKey('Reportes', models.DO_NOTHING)
    usuario_admin = models.ForeignKey('Usuarios', models.DO_NOTHING, blank=True, null=True)
    estado_anterior = models.CharField(max_length=11, blank=True, null=True)
    estado_nuevo = models.CharField(max_length=11)
    observaciones = models.TextField(blank=True, null=True)
    fecha_cambio = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'historialreporte'


class Reportes(models.Model):
    usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, blank=True, null=True)
    id_tipo_anomalia = models.ForeignKey('Tiposanomalia', models.DO_NOTHING, db_column='id_tipo_anomalia')
    barrio = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=500)
    gravedad = models.CharField(max_length=8)
    descripcion = models.TextField()
    info_adicional = models.TextField(blank=True, null=True)
    imagen = models.CharField(max_length=255, blank=True, null=True)
    imagen2 = models.CharField(max_length=255, blank=True, null=True)
    imagen3 = models.CharField(max_length=255, blank=True, null=True)
    latitud = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    longitud = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    estado = models.CharField(max_length=11, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    fecha_reporte = models.DateTimeField()
    fecha_actualizacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'reportes'


class Roles(models.Model):
    nombre_rol = models.CharField(unique=True, max_length=50)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'roles'


class Tiposanomalia(models.Model):
    nombre_anomalia = models.CharField(unique=True, max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.IntegerField(blank=True, null=True)
    fecha_creacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tiposanomalia'


class Usuarios(models.Model):
    nombre_usuario = models.CharField(unique=True, max_length=100)
    correo_electronico = models.CharField(unique=True, max_length=150)
    contrasena_hash = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    codigo_verificacion = models.CharField(max_length=36, blank=True, null=True)
    verificado = models.IntegerField(blank=True, null=True)
    id_rol = models.ForeignKey(Roles, models.DO_NOTHING, db_column='id_rol')
    activo = models.IntegerField(blank=True, null=True)
    fecha_registro = models.DateTimeField()
    ultimo_acceso = models.DateTimeField(blank=True, null=True)
    direccion_residencia = models.CharField(max_length=200, blank=True, null=True)
    numero_documento = models.CharField(max_length=50, blank=True, null=True)
    foto_perfil = models.CharField(max_length=255, blank=True, null=True)
    estado_cuenta = models.CharField(max_length=9, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuarios'


class Zonas(models.Model):
    nombre_zona = models.CharField(unique=True, max_length=100)
    zona_geografica = models.CharField(max_length=13)
    activo = models.IntegerField(blank=True, null=True)
    fecha_creacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'zonas'
