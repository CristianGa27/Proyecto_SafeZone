"""
Vistas de administración.
"""
from django.contrib import messages
from django.db import connection
from django.shortcuts import render, redirect
from ..constants import UserRole, ReportStatus, SESSION_USER_ROLE
from ..decorators import admin_required, tecnico_required, admin_or_tecnico_required
from ..models import Reportes
from ..services import get_dashboard_stats

def _dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

@admin_required
def panel_admin(request):
    estado = request.GET.get('estado')
    gravedad = request.GET.get('gravedad')
    q = """
        SELECT R.id, U.nombre_usuario AS reportado_por, R.ubicacion,
            R.barrio as zona, T.nombre_anomalia, R.gravedad,
            R.descripcion, R.info_adicional, R.fecha_reporte, R.estado,
            R.observaciones, R.imagen, R.imagen2, R.imagen3,
            R.latitud, R.longitud
        FROM reportes R
        LEFT JOIN usuarios U ON R.usuario_id = U.id
        LEFT JOIN tiposanomalia T ON R.id_tipo_anomalia = T.id
        WHERE 1=1
    """
    p = []
    if estado: q += " AND R.estado = %s"; p.append(estado)
    if gravedad: q += " AND R.gravedad = %s"; p.append(gravedad)
    q += " ORDER BY R.id DESC"

    with connection.cursor() as cursor:
        cursor.execute(q, p)
        reportes = _dictfetchall(cursor)

    return render(request, "safezone_app/validacion_reporte.html", {
        'reportes': reportes, 'filtros': {'estado': estado, 'gravedad': gravedad}
    })

@tecnico_required
def panel_tecnico(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT R.id, U.nombre_usuario AS reportado_por, R.ubicacion,
                R.barrio as zona, T.nombre_anomalia, R.gravedad,
                R.descripcion, R.fecha_reporte, R.estado, R.observaciones,
                R.imagen, R.latitud, R.longitud, R.info_adicional
            FROM reportes R
            LEFT JOIN usuarios U ON R.usuario_id = U.id
            LEFT JOIN tiposanomalia T ON R.id_tipo_anomalia = T.id
            WHERE R.estado IN ('pendiente', 'en_progreso', 'resuelto', 'cerrado')
            ORDER BY CASE R.estado
                WHEN 'pendiente' THEN 1 WHEN 'en_progreso' THEN 2
                WHEN 'resuelto' THEN 3 WHEN 'cerrado' THEN 4
            END, R.fecha_reporte DESC
        """)
        reportes = _dictfetchall(cursor)
    return render(request, "safezone_app/panel_tecnico.html", {'reportes': reportes})

@admin_or_tecnico_required
def validar(request, id):
    user_role = request.session.get(SESSION_USER_ROLE)
    estado = request.POST.get("estado")
    if user_role == UserRole.ADMIN_TECNICO and estado not in ReportStatus.TECHNICAL_FLOW:
        return redirect('panel_tecnico')

    Reportes.objects.filter(id=id).update(estado=estado, observaciones=request.POST.get("observaciones"))
    messages.success(request, "Guardado.")
    return redirect('panel_tecnico' if user_role == UserRole.ADMIN_TECNICO else 'panel_admin')

@admin_required
def panel_info_html(request):
    return render(request, "safezone_app/panel_de_informacion.html", {'stats': get_dashboard_stats()})

def admin_info(request):
    return render(request, "safezone_app/panel_de_informacion.html")

@admin_required
def gestion_usuarios(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT u.id, u.nombre_usuario, u.correo_electronico, u.telefono,
                u.direccion_residencia, u.numero_documento, u.estado_cuenta,
                u.fecha_registro, r.nombre_rol, u.verificado
            FROM usuarios u
            LEFT JOIN roles r ON u.id_rol = r.id
            WHERE r.nombre_rol = 'usuario' ORDER BY u.fecha_registro DESC
        """)
        usuarios = _dictfetchall(cursor)
    for u in usuarios:
        c = sum(1 for f in ('telefono', 'direccion_residencia', 'numero_documento') if u.get(f) and str(u[f]).strip())
        u['completitud'] = int((c / 3) * 100)
    return render(request, "safezone_app/gestion_usuarios.html", {'usuarios': usuarios})
