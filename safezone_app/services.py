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


def send_verification_email(correo, nombre, token, request=None):
    """Envía el correo de verificación de cuenta con diseño HTML."""
    from django.core.mail import EmailMultiAlternatives

    # Siempre usa SITE_URL si está definida, para que el enlace funcione desde cualquier dispositivo
    base_url = getattr(settings, 'SITE_URL', None)
    if not base_url and request is not None:
        base_url = request.build_absolute_uri('/').rstrip('/')
    if not base_url:
        base_url = 'http://127.0.0.1:8000'

    link = f"{base_url}/verificar/{token}/"
    subject = "Verifica tu cuenta - SafeZone"

    # Versión texto plano (fallback)
    text_content = (
        f"Hola {nombre},\n\n"
        f"Gracias por registrarte en SafeZone.\n"
        f"Haz clic en el siguiente enlace para verificar tu cuenta:\n\n"
        f"{link}\n\n"
        f"Este enlace expira en 24 horas.\n\n"
        f"Si no creaste esta cuenta, ignora este correo.\n\n"
        f"— El equipo de SafeZone"
    )

    # Versión HTML con diseño y botón
    html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Verifica tu cuenta - SafeZone</title>
</head>
<body style="margin:0;padding:0;background-color:#0f1117;font-family:'Segoe UI',Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#0f1117;padding:40px 20px;">
    <tr>
      <td align="center">
        <table width="560" cellpadding="0" cellspacing="0" style="background:linear-gradient(145deg,#1a1d2e,#12151f);border-radius:20px;overflow:hidden;border:1px solid rgba(255,255,255,0.08);">

          <!-- Header -->
          <tr>
            <td style="background:linear-gradient(135deg,#6c63ff,#48c9b0);padding:36px 40px;text-align:center;">
              <div style="font-size:36px;margin-bottom:8px;">🛡️</div>
              <h1 style="margin:0;color:#ffffff;font-size:26px;font-weight:700;letter-spacing:1px;">SafeZone</h1>
              <p style="margin:6px 0 0;color:rgba(255,255,255,0.85);font-size:13px;letter-spacing:2px;text-transform:uppercase;">Verificación de cuenta</p>
            </td>
          </tr>

          <!-- Body -->
          <tr>
            <td style="padding:40px 40px 20px;">
              <h2 style="margin:0 0 12px;color:#e8e8f0;font-size:22px;font-weight:600;">Hola, {nombre} 👋</h2>
              <p style="margin:0 0 20px;color:#9a9ab0;font-size:15px;line-height:1.7;">
                ¡Gracias por registrarte en <strong style="color:#6c63ff;">SafeZone</strong>!
                Para activar tu cuenta y empezar a usar la plataforma, necesitamos verificar tu correo electrónico.
              </p>
              <p style="margin:0 0 30px;color:#9a9ab0;font-size:15px;line-height:1.7;">
                Haz clic en el botón de abajo para confirmar tu dirección de correo:
              </p>

              <!-- Botón -->
              <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  <td align="center" style="padding-bottom:30px;">
                    <a href="{link}"
                       style="display:inline-block;background:linear-gradient(135deg,#6c63ff,#48c9b0);color:#ffffff;text-decoration:none;font-size:16px;font-weight:700;padding:16px 44px;border-radius:50px;letter-spacing:0.5px;box-shadow:0 8px 24px rgba(108,99,255,0.4);">
                      ✅ Verificar Correo
                    </a>
                  </td>
                </tr>
              </table>

              <!-- Info expiración -->
              <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  <td style="background:rgba(108,99,255,0.1);border:1px solid rgba(108,99,255,0.25);border-radius:12px;padding:16px 20px;">
                    <p style="margin:0;color:#9a9ab0;font-size:13px;line-height:1.6;">
                      ⏰ <strong style="color:#c8c8e0;">Este enlace expira en 24 horas.</strong><br>
                      Si no funciona el botón, copia y pega este enlace en tu navegador:<br>
                      <a href="{link}" style="color:#6c63ff;word-break:break-all;font-size:12px;">{link}</a>
                    </p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="padding:24px 40px 36px;border-top:1px solid rgba(255,255,255,0.06);margin-top:20px;">
              <p style="margin:0;color:#5a5a72;font-size:12px;line-height:1.6;text-align:center;">
                Si no creaste una cuenta en SafeZone, puedes ignorar este correo de forma segura.<br>
                &copy; 2026 SafeZone. Todos los derechos reservados.
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""

    try:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.EMAIL_HOST_USER,
            to=[correo],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=True)
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
            SELECT DATE_FORMAT(fecha_reporte, '%Y-%m') as mes, COUNT(*) as total
            FROM Reportes
            WHERE fecha_reporte >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
            GROUP BY DATE_FORMAT(fecha_reporte, '%Y-%m')
            ORDER BY mes DESC
            LIMIT 6
        """)
        columns = [col[0] for col in cursor.description]
        meses = [dict(zip(columns, row)) for row in cursor.fetchall()]

    if meses:
        max_r = max(r['total'] for r in meses)
        meses_esp = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        stats['reportes_mes'] = []
        for r in reversed(meses):
            try:
                y, m = r['mes'].split('-')
                mes_str = f"{meses_esp[int(m)-1]} {y}"
            except Exception:
                mes_str = r['mes']
                
            stats['reportes_mes'].append({
                'mes': mes_str,
                'total': r['total'],
                'height': max(int((r['total'] / max_r) * 100), 10),
            })

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
            SELECT DATE_FORMAT(fecha_reporte, '%Y-%m') as mes, COUNT(*) as total
            FROM Reportes
            WHERE fecha_reporte >= DATE_SUB(NOW(), INTERVAL 6 MONTH)
            GROUP BY DATE_FORMAT(fecha_reporte, '%Y-%m')
            ORDER BY mes
        """)
        columns = [col[0] for col in cursor.description]
        rmes = [dict(zip(columns, row)) for row in cursor.fetchall()]

        meses_esp = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        for r in rmes:
            try:
                y, m = r['mes'].split('-')
                r['mes'] = f"{meses_esp[int(m)-1]} {y}"
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
