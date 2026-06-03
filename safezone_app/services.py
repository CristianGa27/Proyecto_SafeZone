"""
Servicios de lógica de negocio para SafeZone.

Separa la lógica de negocio de las vistas para mantener
las vistas delgadas y la lógica reutilizable y testeable.
"""

import logging
import os
import uuid
from datetime import datetime

import bcrypt
from django.conf import settings
from django.core.mail import send_mail
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.db.models import Count, Case, When, IntegerField, Value

from .constants import (
    ALLOWED_IMAGE_EXTENSIONS,
    MAX_REPORT_IMAGES,
    ReportStatus,
)
from .models import Usuarios, Reportes, Tiposanomalia, Roles

logger = logging.getLogger(__name__)
signer = TimestampSigner()


# ============================================================
# Servicios de autenticación
# ============================================================

def authenticate_user(correo, contrasena_raw):
    """
    Verifica credenciales de un usuario.

    Args:
        correo: Correo electrónico del usuario.
        contrasena_raw: Contraseña en texto plano.

    Returns:
        tuple: (usuario, nombre_rol) si las credenciales son válidas.
               (None, None) si son inválidas.
    """
    try:
        user = Usuarios.objects.get(correo_electronico=correo)
    except Usuarios.DoesNotExist:
        return None, None

    hashed = user.contrasena_hash.encode('utf-8')
    if not bcrypt.checkpw(contrasena_raw.encode('utf-8'), hashed):
        return None, None

    role_name = user.id_rol.nombre_rol if user.id_rol else 'usuario'
    return user, role_name


def create_user_account(nombre_usuario, correo, contrasena, telefono):
    """
    Crea una nueva cuenta de usuario con token de verificación.

    Returns:
        tuple: (usuario, timed_token) para enviar email de verificación.

    Raises:
        Exception: Si ocurre un error al guardar en la base de datos.
    """
    hashed_password = bcrypt.hashpw(
        contrasena.encode('utf-8'), bcrypt.gensalt()
    ).decode('utf-8')

    token = str(uuid.uuid4())
    timed_token = signer.sign(token)

    rol_usuario = Roles.objects.get(nombre_rol='usuario')
    user = Usuarios(
        nombre_usuario=nombre_usuario,
        correo_electronico=correo,
        contrasena_hash=hashed_password,
        telefono=telefono,
        codigo_verificacion=token,
        verificado=0,
        id_rol=rol_usuario,
        activo=1,
        fecha_registro=datetime.now(),
    )
    user.save()

    return user, timed_token


def verify_user_token(timed_token):
    """
    Verifica un token de activación de cuenta.

    Returns:
        Usuarios o None si el token es inválido/expirado.
    """
    from datetime import timedelta

    try:
        token = signer.unsign(timed_token, max_age=timedelta(days=1))
    except (SignatureExpired, BadSignature):
        return None

    try:
        user = Usuarios.objects.get(codigo_verificacion=token, verificado=0)
        user.verificado = 1
        user.codigo_verificacion = None
        user.save()
        return user
    except Usuarios.DoesNotExist:
        return None


def send_verification_email(correo, nombre, token):
    """Envía el correo de verificación de cuenta."""
    host = settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'http://127.0.0.1:8000'
    link = f"{host}/verificar/{token}/"
    subject = "Verifica tu cuenta - SafeZone"
    message = f"Hola {nombre}, entra aquí para verificar tu cuenta: {link}"

    try:
        send_mail(
            subject, message, settings.EMAIL_HOST_USER,
            [correo], fail_silently=True,
        )
    except Exception as e:
        logger.error("Error enviando correo de verificación: %s", e)


# ============================================================
# Servicios de archivos / imágenes
# ============================================================

def save_uploaded_image(file, prefix="upload"):
    """
    Guarda un archivo de imagen subido en MEDIA_ROOT.

    Args:
        file: Archivo subido (UploadedFile).
        prefix: Prefijo para el nombre del archivo.

    Returns:
        str: Nombre del archivo guardado, o None si la extensión no es válida.
    """
    if not file:
        return None

    ext = file.name.rsplit('.', 1)[-1].lower() if '.' in file.name else ''
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        return None

    filename = f"{prefix}_{uuid.uuid4().hex[:8]}.{ext}"
    path = os.path.join(settings.MEDIA_ROOT, filename)
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

    with open(path, 'wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)

    return filename


def save_report_images(files):
    """
    Guarda las imágenes de un reporte (máximo 3).

    Args:
        files: Lista de archivos subidos.

    Returns:
        list: Lista de 3 elementos con nombres de archivo o None.
    """
    images = [None] * MAX_REPORT_IMAGES

    for i, file in enumerate(files[:MAX_REPORT_IMAGES]):
        if file:
            filename = f"{uuid.uuid4().hex}_{file.name}"
            path = os.path.join(settings.MEDIA_ROOT, filename)
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

            with open(path, 'wb+') as f:
                for chunk in file.chunks():
                    f.write(chunk)

            images[i] = filename

    return images


def delete_old_image(filename):
    """Elimina una imagen anterior si existe."""
    if not filename:
        return

    path = os.path.join(settings.MEDIA_ROOT, filename)
    if os.path.exists(path):
        try:
            os.remove(path)
        except OSError:
            pass


# ============================================================
# Servicios de estadísticas (reemplazan SQL crudo)
# ============================================================

def get_dashboard_stats():
    """
    Obtiene estadísticas del panel de información.

    Returns:
        dict con reportes_totales, reparaciones, en_proceso,
        zona_critica y reportes_mes.
    """
    from django.db import connection

    stats = {
        'reportes_totales': 0,
        'reparaciones': 0,
        'en_proceso': 0,
        'zona_critica': 'Sin datos',
        'reportes_mes': [],
    }

    # Totales generales
    totals = Reportes.objects.aggregate(
        total=Count('id'),
        cerrados=Count(
            Case(When(estado=ReportStatus.CERRADO, then=1),
                 output_field=IntegerField())
        ),
        en_proceso=Count(
            Case(When(estado__in=[ReportStatus.EN_PROGRESO, ReportStatus.PENDIENTE], then=1),
                 output_field=IntegerField())
        ),
    )
    stats['reportes_totales'] = totals['total'] or 0
    stats['reparaciones'] = totals['cerrados'] or 0
    stats['en_proceso'] = totals['en_proceso'] or 0

    # Zona más crítica
    zona_critica = (
        Reportes.objects
        .exclude(barrio__isnull=True)
        .exclude(barrio='')
        .values('barrio')
        .annotate(total=Count('id'))
        .order_by('-total')
        .first()
    )
    if zona_critica:
        stats['zona_critica'] = zona_critica['barrio']

    # Reportes por mes (últimos 6 meses) — requiere SQL por DATE_FORMAT de MySQL
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DATE_FORMAT(fecha_reporte, '%%Y-%%m') as mes, COUNT(*) as total
            FROM Reportes
            WHERE fecha_reporte >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
            GROUP BY DATE_FORMAT(fecha_reporte, '%%Y-%%m')
            ORDER BY mes DESC
            LIMIT 6
        """)
        columns = [col[0] for col in cursor.description]
        meses = [dict(zip(columns, row)) for row in cursor.fetchall()]

    if meses:
        max_r = max(r['total'] for r in meses)
        stats['reportes_mes'] = [
            {
                'mes': r['mes'],
                'total': r['total'],
                'height': max(int((r['total'] / max_r) * 100), 10),
            }
            for r in reversed(meses)
        ]

    return stats


def get_chart_statistics():
    """
    Obtiene estadísticas para los gráficos.

    Returns:
        dict con reportes_mes, severidad y evolucion.
    """
    import calendar
    from django.db import connection

    stats = {
        'reportes_mes': [],
        'severidad': [],
        'evolucion': [],
    }

    with connection.cursor() as cursor:
        # Reportes por mes
        cursor.execute("""
            SELECT DATE_FORMAT(fecha_reporte, '%%Y-%%m') as mes, COUNT(*) as total
            FROM Reportes
            WHERE fecha_reporte >= DATE_SUB(NOW(), INTERVAL 6 MONTH)
            GROUP BY DATE_FORMAT(fecha_reporte, '%%Y-%%m')
            ORDER BY mes
        """)
        columns = [col[0] for col in cursor.description]
        rmes = [dict(zip(columns, row)) for row in cursor.fetchall()]

        for r in rmes:
            try:
                y, m = r['mes'].split('-')
                r['mes'] = f"{calendar.month_name[int(m)][:3]} {y}"
            except (ValueError, IndexError):
                pass

        stats['reportes_mes'] = rmes

        # Por severidad
        cursor.execute("""
            SELECT gravedad, COUNT(*) as total
            FROM Reportes
            GROUP BY gravedad
            ORDER BY CASE gravedad
                WHEN 'critico' THEN 1
                WHEN 'severo' THEN 2
                WHEN 'moderado' THEN 3
                WHEN 'leve' THEN 4
            END
        """)
        columns = [col[0] for col in cursor.description]
        stats['severidad'] = [dict(zip(columns, row)) for row in cursor.fetchall()]

        # Evolución semanal
        cursor.execute("""
            SELECT WEEK(fecha_reporte) as semana, COUNT(*) as total
            FROM Reportes
            WHERE fecha_reporte >= DATE_SUB(NOW(), INTERVAL 8 WEEK)
            GROUP BY WEEK(fecha_reporte)
            ORDER BY semana
        """)
        columns = [col[0] for col in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        stats['evolucion'] = [
            {'semana': i + 1, 'total': row['total']}
            for i, row in enumerate(rows)
        ]

    return stats
