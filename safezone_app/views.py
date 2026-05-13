import logging
import uuid
import bcrypt
import os
import calendar
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db import connection
from django.conf import settings
from django.core.mail import send_mail
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from .models import Usuarios, Zonas, Tiposanomalia, Reportes, Roles

signer = TimestampSigner()

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def fetch_one_dict(cursor):
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()
    if row:
        return dict(zip(columns, row))
    return None

def is_guest(request):
    return request.session.get('user_role') == 'guest' or not request.session.get('user_id')

# --- AUTH VIEWS ---

def _send_verification_email(correo, nombre, token):
    link = f"{settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'http://127.0.0.1:8000'}/verificar/{token}/"
    subject = "Verifica tu cuenta - SafeZone"
    message = f"Hola {nombre}, entra aquí para verificar tu cuenta: {link}"
    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, [correo], fail_silently=True)
    except Exception as e:
        logging.error(f"Error enviando correo: {e}")

def login_view(request):
    if request.method == "POST":
        correo = request.POST.get('loginEmail', '').strip()
        contrasena = request.POST.get('loginPassword', '').encode('utf-8')
        
        try:
            user = Usuarios.objects.get(correo_electronico=correo)
        except Usuarios.DoesNotExist:
            messages.error(request, "Correo o contraseña incorrectos.")
            return redirect('login_html')
            
        hashed = user.contrasena_hash.encode('utf-8')
        if not bcrypt.checkpw(contrasena, hashed):
            messages.error(request, "Correo o contraseña incorrectos.")
            return redirect('login_html')
            
        role_name = user.id_rol.nombre_rol if user.id_rol else 'usuario'
        
        if role_name not in ('admin_principal', 'admin_tecnico'):
            if user.verificado == 0:
                messages.warning(request, "Debes verificar tu correo antes de iniciar sesión.")
                return redirect('esperando_verificacion')
                
        request.session['user_id'] = user.id
        request.session['username'] = user.nombre_usuario
        request.session['foto_perfil'] = user.foto_perfil
        
        if role_name == 'admin_principal':
            request.session['user_role'] = 'admin_principal'
            messages.success(request, "Bienvenido al panel de administración.")
            return redirect('panel_admin')
        elif role_name == 'admin_tecnico':
            request.session['user_role'] = 'admin_tecnico'
            messages.success(request, "Bienvenido al panel técnico.")
            return redirect('panel_tecnico')
        else:
            request.session['user_role'] = 'user'
            messages.success(request, "Bienvenido al sistema.")
            return redirect('inicio_html')

    return render(request, "safezone_app/login.html")

def register_page(request):
    return render(request, "safezone_app/registro.html")

def guest_login(request):
    request.session['user_role'] = 'guest'
    request.session['user_id'] = 0
    request.session['username'] = 'Invitado'
    messages.warning(request, "Has ingresado como invitado. Funciones limitadas.")
    return redirect('registro_html')

def register(request):
    if request.method == "POST":
        nombres = request.POST.get('registerNombres', '').strip()
        apellidos = request.POST.get('registerApellidos', '').strip()
        nombre_usuario = f"{nombres} {apellidos}".strip()
        telefono = request.POST.get('registerPhone', '').strip()
        correo = request.POST.get('registerEmail', '').strip()
        contrasena = request.POST.get('registerPassword', '')
        
        if not all([nombre_usuario, correo, contrasena, telefono]):
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('register_page')
            
        if Usuarios.objects.filter(correo_electronico=correo).exists():
            messages.error(request, "El correo electrónico ya está registrado.")
            return redirect('register_page')
            
        hashed_password = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        token = str(uuid.uuid4())
        timed_token = signer.sign(token)
        
        try:
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
                fecha_registro=datetime.now()
            )
            user.save()
            _send_verification_email(correo, nombre_usuario, timed_token)
            messages.success(request, "Te enviamos un correo. Haz clic en el botón 'Verificar Correo' para activar tu cuenta.")
            return redirect('esperando_verificacion')
        except Exception as e:
            logging.error(f"Error al crear cuenta: {e}")
            messages.error(request, f"Error al crear la cuenta: {str(e)}")
            
    return redirect('register_page')

def esperando_verificacion(request):
    return render(request, "safezone_app/esperando_verificacion.html")

def verificar_token(request, timed_token):
    try:
        token = signer.unsign(timed_token, max_age=timedelta(days=1))
    except (SignatureExpired, BadSignature):
        messages.error(request, "El enlace de verificación ha expirado o es inválido.")
        return render(request, "safezone_app/verificacion_invalida.html")
        
    try:
        user = Usuarios.objects.get(codigo_verificacion=token, verificado=0)
        user.verificado = 1
        user.codigo_verificacion = None
        user.save()
        
        request.session['user_id'] = user.id
        request.session['username'] = user.nombre_usuario
        request.session['user_role'] = 'user'
        request.session['foto_perfil'] = None
        messages.success(request, "¡Cuenta activada exitosamente! Bienvenido al sistema.")
        return redirect('inicio_html')
    except Usuarios.DoesNotExist:
        return render(request, "safezone_app/verificacion_invalida.html")

def logout_view(request):
    request.session.flush()
    messages.info(request, "Has cerrado sesión exitosamente.")
    return redirect('login_html')

def perfil(request):
    if 'user_id' not in request.session or request.session.get('user_role') == 'guest':
        messages.error(request, "Debes iniciar sesión con tu cuenta para ver y actualizar tu perfil.")
        return redirect('login_html')
        
    user = Usuarios.objects.get(id=request.session['user_id'])
    
    if request.method == "POST":
        telefono = request.POST.get("telefono", "").strip()
        direccion = request.POST.get("direccion_residencia", "").strip()
        documento = request.POST.get("numero_documento", "").strip()
        
        # Asegurar que el directorio de medios existe
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        
        foto = request.FILES.get("foto_perfil")
        foto_filename = user.foto_perfil
        
        if foto:
            ext = foto.name.rsplit('.', 1)[-1].lower() if '.' in foto.name else ''
            if ext in {'png', 'jpg', 'jpeg', 'gif'}:
                filename = f"avatar_{user.id}_{uuid.uuid4().hex[:8]}.{ext}"
                path = os.path.join(settings.MEDIA_ROOT, filename)
                try:
                    with open(path, 'wb+') as f:
                        for chunk in foto.chunks(): f.write(chunk)
                    
                    # Eliminar foto anterior si existe
                    if foto_filename and os.path.exists(os.path.join(settings.MEDIA_ROOT, foto_filename)):
                        try: os.remove(os.path.join(settings.MEDIA_ROOT, foto_filename))
                        except: pass
                    
                    foto_filename = filename
                    request.session['foto_perfil'] = filename
                    request.session.modified = True
                except Exception as e:
                    messages.error(request, f"Error al guardar la imagen: {e}")
            else:
                messages.error(request, "Formato de imagen no permitido (solo png, jpg, jpeg, gif).")
        
        # Actualizar otros campos si se proporcionaron
        user.telefono = telefono if telefono else user.telefono
        user.direccion_residencia = direccion if direccion else user.direccion_residencia
        user.numero_documento = documento if documento else user.numero_documento
        user.foto_perfil = foto_filename
        
        try:
            user.save()
            messages.success(request, "Perfil actualizado correctamente.")
        except Exception as e:
            messages.error(request, f"Error al guardar los cambios en la base de datos: {e}")
            
    return render(request, "safezone_app/perfil.html", {'user': user})

# --- REPORTS VIEWS ---

def inicio_html(request):
    if 'user_role' not in request.session:
        messages.error(request, "Debes iniciar sesión para acceder.")
        return redirect('login_html')
    return render(request, "safezone_app/inicio.html")

def panel_info_html(request):
    if request.session.get('user_role') not in ['admin_principal', 'admin']:
        messages.error(request, "Acceso denegado.")
        return redirect('login_html')
        
    stats = {'reportes_totales': 0, 'reparaciones': 0, 'en_proceso': 0, 'zona_critica': 'Sin datos', 'reportes_mes': []}
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) as total, SUM(CASE WHEN estado = 'cerrado' THEN 1 ELSE 0 END) as cerrados, SUM(CASE WHEN estado IN ('en_progreso', 'pendiente') THEN 1 ELSE 0 END) as en_proceso FROM Reportes")
        res = fetch_one_dict(cursor)
        if res:
            stats.update({'reportes_totales': res['total'] or 0, 'reparaciones': res['cerrados'] or 0, 'en_proceso': res['en_proceso'] or 0})
            
        cursor.execute("SELECT barrio, COUNT(*) as total FROM Reportes WHERE barrio IS NOT NULL AND barrio != '' GROUP BY barrio ORDER BY total DESC LIMIT 1")
        res = fetch_one_dict(cursor)
        if res: stats['zona_critica'] = res['barrio']
        
        cursor.execute("SELECT DATE_FORMAT(fecha_reporte, '%%Y-%%m') as mes, COUNT(*) as total FROM Reportes WHERE fecha_reporte >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH) GROUP BY DATE_FORMAT(fecha_reporte, '%%Y-%%m') ORDER BY mes DESC LIMIT 6")
        meses = dictfetchall(cursor)
        if meses:
            max_r = max(r['total'] for r in meses)
            stats['reportes_mes'] = [{'mes': r['mes'], 'total': r['total'], 'height': max(int((r['total'] / max_r) * 100), 10)} for r in reversed(meses)]
            
    return render(request, "safezone_app/panel_de_informacion.html", {'stats': stats})

def registro_html(request):
    if is_guest(request):
        messages.error(request, "Debes iniciar sesión para poder reportar un daño vial.")
        return redirect('login_html')
        
    user = Usuarios.objects.get(id=request.session['user_id'])
    if not user.telefono or not user.direccion_residencia or not user.numero_documento:
        messages.warning(request, "Tu perfil está incompleto. Completa tus datos para reportar.")
        return redirect('perfil')
        
    zonas = Zonas.objects.filter(activo=1).order_by('zona_geografica', 'nombre_zona')
    tipos = Tiposanomalia.objects.filter(activo=1).order_by('nombre_anomalia')
    return render(request, 'safezone_app/registro_deusuario.html', {'zonas': zonas, 'tipos_anomalia': tipos})

def mis_reportes_html(request):
    if is_guest(request):
        messages.error(request, "Solo disponible para usuarios registrados.")
        return redirect('registro_html')
        
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT R.id, R.ubicacion, R.barrio as nombre_zona, T.nombre_anomalia, R.gravedad,
                R.descripcion, R.fecha_reporte, R.estado, R.observaciones,
                R.imagen, R.imagen2, R.imagen3, R.latitud, R.longitud
            FROM Reportes R
            LEFT JOIN TiposAnomalia T ON R.id_tipo_anomalia = T.id
            WHERE R.usuario_id = %s ORDER BY R.id DESC
        """, [request.session['user_id']])
        reportes = dictfetchall(cursor)
        
    return render(request, "safezone_app/mis_reportes.html", {'reportes': reportes})

def registro_reporte(request):
    if request.method == "POST":
        ubicacion = request.POST.get("location")
        barrio = request.POST.get("zone_id")
        tipo_anomalia_id = request.POST.get("tipo_anomalia_id")
        gravedad = request.POST.get("severity")
        descripcion = request.POST.get("description")
        info_adicional = request.POST.get("additionalInfo")
        
        if not all([ubicacion, barrio, tipo_anomalia_id, gravedad, descripcion]):
            messages.error(request, "Faltan campos obligatorios.")
            return redirect('registro_html')
            
        latitud = float(request.POST.get("latitude") or 0) or None
        longitud = float(request.POST.get("longitude") or 0) or None
        
        imagenes = [None, None, None]
        files = request.FILES.getlist('imageUpload')[:3]
        for i, file in enumerate(files):
            if file:
                filename = f"{os.urandom(8).hex()}_{file.name}"
                path = os.path.join(settings.MEDIA_ROOT, filename)
                with open(path, 'wb+') as f:
                    for chunk in file.chunks(): f.write(chunk)
                imagenes[i] = filename
                
        user = Usuarios.objects.get(id=request.session['user_id'])
        tipo = Tiposanomalia.objects.get(id=tipo_anomalia_id)
        
        rep = Reportes(
            ubicacion=ubicacion, barrio=barrio, id_tipo_anomalia=tipo, gravedad=gravedad,
            descripcion=descripcion, info_adicional=info_adicional,
            imagen=imagenes[0], imagen2=imagenes[1], imagen3=imagenes[2],
            usuario=user, estado='nuevo', latitud=latitud, longitud=longitud,
            fecha_reporte=datetime.now(), fecha_actualizacion=datetime.now()
        )
        rep.save()
        messages.success(request, "Reporte enviado exitosamente.")
    return redirect('registro_html')

def editar_reporte_html(request, reporte_id):
    if is_guest(request): return redirect('registro_html')
    try:
        reporte = Reportes.objects.get(id=reporte_id, usuario_id=request.session['user_id'])
    except Reportes.DoesNotExist:
        messages.error(request, "Reporte no encontrado.")
        return redirect('mis_reportes_html')
        
    zonas = Zonas.objects.filter(activo=1).order_by('zona_geografica', 'nombre_zona')
    tipos = Tiposanomalia.objects.filter(activo=1).order_by('nombre_anomalia')
    return render(request, "safezone_app/editar_reporte.html", {'reporte': reporte, 'zonas': zonas, 'tipos_anomalia': tipos})

def actualizar_reporte(request, reporte_id):
    if request.method == "POST":
        try:
            reporte = Reportes.objects.get(id=reporte_id, usuario_id=request.session['user_id'])
            reporte.ubicacion = request.POST.get("location")
            reporte.barrio = request.POST.get("zone_id")
            reporte.id_tipo_anomalia = Tiposanomalia.objects.get(id=request.POST.get("tipo_anomalia_id"))
            reporte.gravedad = request.POST.get("severity")
            reporte.descripcion = request.POST.get("description")
            reporte.info_adicional = request.POST.get("additionalInfo")
            reporte.save()
            messages.success(request, "Reporte actualizado.")
        except Exception:
            messages.error(request, "Error al actualizar.")
    return redirect('mis_reportes_html')

def api_reportes(request):
    if 'user_role' not in request.session:
        return JsonResponse({"error": "No autorizado"}, status=401)
        
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT R.id, R.ubicacion, R.barrio as zona, T.nombre_anomalia as tipo_anomalia,
                R.gravedad, R.descripcion, R.info_adicional, R.fecha_reporte, R.estado,
                R.latitud as lat, R.longitud as lng, R.imagen, R.imagen2, R.imagen3,
                U.nombre_usuario AS reportado_por
            FROM Reportes R
            LEFT JOIN Usuarios U ON R.usuario_id = U.id
            LEFT JOIN TiposAnomalia T ON R.id_tipo_anomalia = T.id
            ORDER BY R.fecha_reporte DESC
        """ )
        reportes = dictfetchall(cursor)
        for r in reportes:
            if r['fecha_reporte']: r['fecha_reporte'] = r['fecha_reporte'].strftime('%Y-%m-%d %H:%M:%S')
            r['image_url'] = f"/static/uploads/{r['imagen']}" if r['imagen'] else None
            r['image_url2'] = f"/static/uploads/{r['imagen2']}" if r['imagen2'] else None
            r['image_url3'] = f"/static/uploads/{r['imagen3']}" if r['imagen3'] else None
    return JsonResponse(reportes, safe=False)

# --- ADMIN VIEWS ---

def panel_admin(request):
    if request.session.get('user_role') not in ['admin_principal', 'admin', 'moderador']:
        messages.error(request, "Acceso denegado.")
        return redirect('login_html')
        
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT R.id, U.nombre_usuario AS reportado_por, R.ubicacion, R.barrio as nombre_zona,
                T.nombre_anomalia, R.gravedad, R.descripcion, R.fecha_reporte,
                R.estado, R.observaciones, R.imagen, R.latitud, R.longitud
            FROM Reportes R
            LEFT JOIN Usuarios U ON R.usuario_id = U.id
            LEFT JOIN TiposAnomalia T ON R.id_tipo_anomalia = T.id
            ORDER BY R.id DESC
        """)
        reportes = dictfetchall(cursor)
    return render(request, "safezone_app/validacion_reporte.html", {'reportes': reportes})

def panel_tecnico(request):
    if request.session.get('user_role') != 'admin_tecnico':
        messages.error(request, "Acceso denegado.")
        return redirect('login_html')
        
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT R.id, U.nombre_usuario AS reportado_por, R.ubicacion, R.barrio as zona,
                T.nombre_anomalia, R.gravedad, R.descripcion, R.fecha_reporte,
                R.estado, R.observaciones, R.imagen, R.latitud, R.longitud, R.info_adicional
            FROM Reportes R
            LEFT JOIN Usuarios U ON R.usuario_id = U.id
            LEFT JOIN TiposAnomalia T ON R.id_tipo_anomalia = T.id
            WHERE R.estado IN ('pendiente', 'en_progreso', 'resuelto', 'cerrado')
            ORDER BY CASE R.estado
                WHEN 'pendiente' THEN 1 WHEN 'en_progreso' THEN 2
                WHEN 'resuelto' THEN 3 WHEN 'cerrado' THEN 4
            END, R.fecha_reporte DESC
        """)
        reportes = dictfetchall(cursor)
    return render(request, "safezone_app/panel_tecnico.html", {'reportes': reportes})

def validar(request, id):
    user_role = request.session.get('user_role')
    if user_role not in ['admin_principal', 'admin_tecnico', 'admin']:
        return redirect('login_html')
        
    estado = request.POST.get("estado")
    observaciones = request.POST.get("observaciones")
    
    if user_role == 'admin_tecnico' and estado not in ['pendiente', 'en_progreso', 'resuelto', 'cerrado']:
        messages.error(request, "Estado no válido para el flujo técnico.")
        return redirect('panel_tecnico')
        
    Reportes.objects.filter(id=id).update(estado=estado, observaciones=observaciones)
    messages.success(request, "Validación guardada.")
    return redirect('panel_tecnico' if user_role == 'admin_tecnico' else 'panel_admin')

def admin_info(request):
    return render(request, "safezone_app/panel_de_informacion.html")

def gestion_usuarios(request):
    if request.session.get('user_role') not in ['admin_principal', 'moderador']:
        return redirect('login_html')
        
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT u.id, u.nombre_usuario, u.correo_electronico, u.telefono,
                u.direccion_residencia, u.numero_documento, u.estado_cuenta,
                u.fecha_registro, r.nombre_rol, u.verificado
            FROM Usuarios u
            LEFT JOIN Roles r ON u.id_rol = r.id
            WHERE r.nombre_rol = 'usuario'
            ORDER BY u.fecha_registro DESC
        """)
        usuarios = dictfetchall(cursor)
        
    for u in usuarios:
        c = sum(1 for x in [u.get('telefono'), u.get('direccion_residencia'), u.get('numero_documento')] if x and str(x).strip())
        u['completitud'] = int((c / 3) * 100)
    return render(request, "safezone_app/gestion_usuarios.html", {'usuarios': usuarios})

# --- VISUALIZATIONS VIEWS ---

def mapa_html(request):
    return render(request, "safezone_app/mapa.html")

def estadisticas_html(request):
    return render(request, "safezone_app/estadisticas.html")

def api_estadisticas(request):
    if 'user_role' not in request.session:
        return JsonResponse({"error": "No autorizado"}, status=401)
        
    stats = {
        'reportes_mes': [],
        'severidad': [],
        'evolucion': []
    }
    with connection.cursor() as cursor:
        cursor.execute("SELECT DATE_FORMAT(fecha_reporte, '%%Y-%%m') as mes, COUNT(*) as total FROM Reportes WHERE fecha_reporte >= DATE_SUB(NOW(), INTERVAL 6 MONTH) GROUP BY DATE_FORMAT(fecha_reporte, '%%Y-%%m') ORDER BY mes")
        rmes = dictfetchall(cursor)
        for r in rmes:
            try:
                y, m = r['mes'].split('-')
                r['mes'] = f"{calendar.month_name[int(m)][:3]} {y}"
            except: pass
        stats['reportes_mes'] = rmes
        
        cursor.execute("SELECT gravedad, COUNT(*) as total FROM Reportes GROUP BY gravedad ORDER BY CASE gravedad WHEN 'critico' THEN 1 WHEN 'severo' THEN 2 WHEN 'moderado' THEN 3 WHEN 'leve' THEN 4 END")
        stats['severidad'] = dictfetchall(cursor)
        
        cursor.execute("SELECT WEEK(fecha_reporte) as semana, COUNT(*) as total FROM Reportes WHERE fecha_reporte >= DATE_SUB(NOW(), INTERVAL 8 WEEK) GROUP BY WEEK(fecha_reporte) ORDER BY semana")
        stats['evolucion'] = [{'semana': i+1, 'total': row['total']} for i, row in enumerate(dictfetchall(cursor))]
        
    return JsonResponse(stats)
