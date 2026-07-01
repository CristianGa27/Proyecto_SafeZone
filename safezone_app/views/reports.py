"""
Vistas de reportes.
"""
from datetime import datetime
from django.contrib import messages
from django.shortcuts import render, redirect
from ..constants import UserRole, ReportStatus, SESSION_USER_ID, SESSION_USER_ROLE
from ..decorators import login_required_safezone, session_required
from ..models import Usuarios, Zonas, Tiposanomalia, Reportes
from ..services import save_report_images

@session_required
def inicio_html(request):
    """
    Renderiza la página principal de inicio para cualquier usuario logueado.
    Calcula y muestra estadísticas rápidas (reportes activos, resueltos, usuarios).
    """
    reportes_activos = Reportes.objects.exclude(estado__in=[ReportStatus.RESUELTO, ReportStatus.CERRADO, ReportStatus.RECHAZADO]).count()
    problemas_resueltos = Reportes.objects.filter(estado__in=[ReportStatus.RESUELTO, ReportStatus.CERRADO]).count()
    usuarios_registrados = Usuarios.objects.count()
    
    context = {
        'reportes_activos': reportes_activos,
        'problemas_resueltos': problemas_resueltos,
        'usuarios_registrados': usuarios_registrados
    }
    return render(request, "safezone_app/inicio.html", context)

@login_required_safezone
def registro_html(request):
    """
    Renderiza el formulario para registrar un nuevo reporte.
    Verifica primero que el perfil del usuario esté completo.
    """
    user = Usuarios.objects.get(id=request.session[SESSION_USER_ID])
    if not user.telefono or not user.direccion_residencia or not user.numero_documento:
        messages.warning(request, "Completa tu perfil.")
        return redirect('perfil')

    zonas = Zonas.objects.filter(activo=1).order_by('zona_geografica', 'nombre_zona')
    tipos = Tiposanomalia.objects.filter(activo=1).order_by('nombre_anomalia')
    return render(request, 'safezone_app/registro_deusuario.html', {'zonas': zonas, 'tipos_anomalia': tipos})

@login_required_safezone
def registro_reporte(request):
    """
    Procesa los datos enviados desde el formulario de nuevo reporte.
    Sube las imágenes, asocia la zona y guarda el reporte como 'pendiente'.
    """
    if request.method != "POST":
        return redirect('registro_html')

    try:
        user = Usuarios.objects.get(id=request.session[SESSION_USER_ID])
        tipo = Tiposanomalia.objects.get(id=request.POST.get("tipo_anomalia_id"))
        imagenes = save_report_images(request.FILES.getlist('imageUpload'))

        reporte = Reportes(
            ubicacion=request.POST.get("location"),
            barrio=request.POST.get("zone_id"),
            id_tipo_anomalia=tipo,
            gravedad=request.POST.get("severity"),
            descripcion=request.POST.get("description"),
            info_adicional=request.POST.get("additionalInfo"),
            imagen=imagenes[0], imagen2=imagenes[1], imagen3=imagenes[2],
            usuario=user,
            estado=ReportStatus.NUEVO,
            latitud=float(request.POST.get("latitude") or 0) or None,
            longitud=float(request.POST.get("longitude") or 0) or None,
            fecha_reporte=datetime.now(),
            fecha_actualizacion=datetime.now(),
        )
        reporte.save()
        messages.success(request, f"Reporte #{reporte.id} enviado.")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect('registro_html')

@login_required_safezone
def mis_reportes_html(request):
    """
    Renderiza el historial personal de reportes creados por el usuario actual.
    Realiza una consulta a la base de datos para traer el historial detallado.
    """
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT R.id, R.ubicacion, R.barrio as nombre_zona, T.nombre_anomalia,
                R.gravedad, R.descripcion, R.fecha_reporte, R.estado, R.observaciones,
                R.imagen, R.imagen2, R.imagen3, R.latitud, R.longitud
            FROM reportes R
            LEFT JOIN tiposanomalia T ON R.id_tipo_anomalia = T.id
            WHERE R.usuario_id = %s ORDER BY R.id DESC
        """, [request.session[SESSION_USER_ID]])
        cols = [c[0] for c in cursor.description]
        reportes = [dict(zip(cols, row)) for row in cursor.fetchall()]

    return render(request, "safezone_app/mis_reportes.html", {'reportes': reportes})

@login_required_safezone
def editar_reporte_html(request, reporte_id):
    """
    Renderiza el formulario de edición para un reporte existente,
    verificando que pertenezca al usuario logueado.
    """
    try:
        reporte = Reportes.objects.get(id=reporte_id, usuario_id=request.session[SESSION_USER_ID])
    except Reportes.DoesNotExist:
        return redirect('mis_reportes_html')
    return render(request, "safezone_app/editar_reporte.html", {
        'reporte': reporte,
        'zonas': Zonas.objects.filter(activo=1),
        'tipos_anomalia': Tiposanomalia.objects.filter(activo=1),
    })

@login_required_safezone
def actualizar_reporte(request, reporte_id):
    """
    Procesa la actualización de los datos de un reporte existente
    que pertenece al usuario (zona, descripción, gravedad, etc.).
    """
    if request.method == "POST":
        try:
            r = Reportes.objects.get(id=reporte_id, usuario_id=request.session[SESSION_USER_ID])
            r.ubicacion = request.POST.get("location")
            r.barrio = request.POST.get("zone_id")
            r.id_tipo_anomalia = Tiposanomalia.objects.get(id=request.POST.get("tipo_anomalia_id"))
            r.gravedad = request.POST.get("severity")
            r.descripcion = request.POST.get("description")
            r.info_adicional = request.POST.get("additionalInfo")
            r.save()
            messages.success(request, "Actualizado.")
        except Exception:
            messages.error(request, "Error.")
    return redirect('mis_reportes_html')
