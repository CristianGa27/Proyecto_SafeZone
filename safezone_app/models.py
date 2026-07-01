# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Configuracionsistema(models.Model):
    """
    Modelo que representa la tabla 'configuracionsistema'.
    Almacena variables de configuración globales del sistema (como límites, correos de soporte, etc.).
    """
    clave = models.CharField(unique=True, max_length=100)
    valor = models.TextField()
    descripcion = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=7, blank=True, null=True)
    fecha_actualizacion = models.DateTimeField()

    class Meta:
        db_table = 'configuracionsistema'
        verbose_name = 'Configuración del sistema'
        verbose_name_plural = 'Configuraciones del sistema'


class Historialreporte(models.Model):
    """
    Modelo que representa la tabla 'historialreporte'.
    Mantiene un registro de auditoría de todos los cambios de estado que sufre un reporte,
    incluyendo quién realizó el cambio y sus observaciones.
    """
    reporte = models.ForeignKey('Reportes', models.DO_NOTHING)
    usuario_admin = models.ForeignKey('Usuarios', models.DO_NOTHING, blank=True, null=True)
    estado_anterior = models.CharField(max_length=11, blank=True, null=True)
    estado_nuevo = models.CharField(max_length=11)
    observaciones = models.TextField(blank=True, null=True)
    fecha_cambio = models.DateTimeField()

    class Meta:
        db_table = 'historialreporte'
        verbose_name = 'Historial de reporte'
        verbose_name_plural = 'Historial de reportes'


class Reportes(models.Model):
    """
    Modelo que representa la tabla 'reportes'.
    Es la entidad principal del sistema donde se almacenan las anomalías viales
    reportadas por los ciudadanos (baches, vías dañadas, estado, fotos, ubicación).
    """
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
        db_table = 'reportes'
        verbose_name = 'Reporte'
        verbose_name_plural = 'Reportes'


class Roles(models.Model):
    """
    Modelo que representa la tabla 'roles'.
    Define los diferentes niveles de acceso y permisos dentro del sistema
    (ej. Admin Principal, Admin Técnico, Usuario, Invitado).
    """
    nombre_rol = models.CharField(unique=True, max_length=50)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField()

    class Meta:
        db_table = 'roles'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'


class Tiposanomalia(models.Model):
    """
    Modelo que representa la tabla 'tiposanomalia'.
    Catálogo de los tipos de problemas que pueden reportarse (ej. Baches, Alcantarillado).
    """
    nombre_anomalia = models.CharField(unique=True, max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.IntegerField(blank=True, null=True)
    fecha_creacion = models.DateTimeField()

    class Meta:
        db_table = 'tiposanomalia'
        verbose_name = 'Tipo de anomalía'
        verbose_name_plural = 'Tipos de anomalía'


class Usuarios(models.Model):
    """
    Modelo que representa la tabla 'usuarios'.
    Almacena la información personal, credenciales de acceso e información
    de perfil de todas las personas registradas en el sistema.
    """
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
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'


class Zonas(models.Model):
    """
    Modelo que representa la tabla 'zonas'.
    Catálogo geográfico que agrupa diferentes barrios en zonas más grandes
    para facilitar la filtración y gestión técnica.
    """
    nombre_zona = models.CharField(unique=True, max_length=100)
    zona_geografica = models.CharField(max_length=13)
    activo = models.IntegerField(blank=True, null=True)
    fecha_creacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'zonas'
