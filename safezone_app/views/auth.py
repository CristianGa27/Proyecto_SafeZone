"""
Vistas de autenticación y perfil de usuario.
"""
import logging
from django.contrib import messages
from django.shortcuts import render, redirect
from ..constants import UserRole, SESSION_USER_ID, SESSION_USERNAME, SESSION_USER_ROLE, SESSION_FOTO_PERFIL
from ..models import Usuarios
from ..services import (
    authenticate_user, create_user_account, verify_user_token,
    send_verification_email, save_uploaded_image, delete_old_image
)

logger = logging.getLogger(__name__)

def login_view(request):
    if request.method != "POST":
        return render(request, "safezone_app/login.html")

    correo = request.POST.get('loginEmail', '').strip()
    contrasena = request.POST.get('loginPassword', '')
    user, role_name = authenticate_user(correo, contrasena)

    if not user:
        messages.error(request, "Correo o contraseña incorrectos.")
        return redirect('login_html')

    if role_name not in (UserRole.ADMIN_PRINCIPAL, UserRole.ADMIN_TECNICO) and user.verificado == 0:
        messages.warning(request, "Debes verificar tu correo antes de iniciar sesión.")
        return redirect('esperando_verificacion')

    request.session[SESSION_USER_ID] = user.id
    request.session[SESSION_USERNAME] = user.nombre_usuario
    request.session[SESSION_FOTO_PERFIL] = user.foto_perfil

    redirect_map = {
        UserRole.ADMIN_PRINCIPAL: ('admin_principal', "Bienvenido al panel de administración.", 'panel_admin'),
        UserRole.ADMIN_TECNICO: ('admin_tecnico', "Bienvenido al panel técnico.", 'panel_tecnico'),
    }

    if role_name in redirect_map:
        session_role, msg, url = redirect_map[role_name]
        request.session[SESSION_USER_ROLE] = session_role
        messages.success(request, msg)
        return redirect(url)

    request.session[SESSION_USER_ROLE] = UserRole.USER
    messages.success(request, "Bienvenido al sistema.")
    return redirect('inicio_html')

def register_page(request):
    return render(request, "safezone_app/registro.html")

def guest_login(request):
    request.session[SESSION_USER_ROLE] = UserRole.GUEST
    request.session[SESSION_USER_ID] = 0
    request.session[SESSION_USERNAME] = 'Invitado'
    messages.warning(request, "Has ingresado como invitado. Funciones limitadas.")
    return redirect('registro_html')

def register(request):
    if request.method != "POST":
        return redirect('register_page')

    from ..forms import RegisterForm

    form_data = {
        'nombres': request.POST.get('registerNombres', '').strip(),
        'apellidos': request.POST.get('registerApellidos', '').strip(),
        'telefono': request.POST.get('registerPhone', '').strip(),
        'email': request.POST.get('registerEmail', '').strip(),
        'password': request.POST.get('registerPassword', ''),
    }
    form = RegisterForm(form_data)

    if not form.is_valid():
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, error)
        return redirect('register_page')

    nombres = form.cleaned_data['nombres']
    apellidos = form.cleaned_data['apellidos']
    nombre_usuario = f"{nombres} {apellidos}".strip()
    correo = form.cleaned_data['email']
    telefono = form.cleaned_data['telefono']
    contrasena = form.cleaned_data['password']

    try:
        user, timed_token = create_user_account(nombre_usuario, correo, contrasena, telefono)
        send_verification_email(correo, nombre_usuario, timed_token, request)
        messages.success(request, "¡Registro exitoso! Te enviamos un correo de verificación a " + correo + ".")
        return redirect('esperando_verificacion')
    except Exception as e:
        logger.exception("Error al registrar usuario")
        messages.error(request, f"Error al crear la cuenta: {e}")

    return redirect('register_page')

def esperando_verificacion(request):
    return render(request, "safezone_app/esperando_verificacion.html")

def verificar_token(request, timed_token):
    user = verify_user_token(timed_token)
    if not user:
        messages.error(request, "Enlace inválido o expirado.")
        return render(request, "safezone_app/verificacion_invalida.html")

    request.session[SESSION_USER_ID] = user.id
    request.session[SESSION_USERNAME] = user.nombre_usuario
    request.session[SESSION_USER_ROLE] = UserRole.USER
    request.session[SESSION_FOTO_PERFIL] = None
    messages.success(request, "Cuenta activada exitosamente.")
    return redirect('inicio_html')

def logout_view(request):
    request.session.flush()
    messages.info(request, "Has cerrado sesión.")
    return redirect('login_html')

def perfil(request):
    user_id = request.session.get(SESSION_USER_ID)
    if not user_id or request.session.get(SESSION_USER_ROLE) == UserRole.GUEST:
        return redirect('login_html')

    user = Usuarios.objects.get(id=user_id)
    if request.method == "POST":
        telefono = request.POST.get("telefono", "").strip()
        user.telefono = telefono if telefono else user.telefono
        user.direccion_residencia = request.POST.get("direccion_residencia", user.direccion_residencia)
        user.numero_documento = request.POST.get("numero_documento", user.numero_documento)
        
        foto = request.FILES.get("foto_perfil")
        if foto:
            new_filename = save_uploaded_image(foto, f"avatar_{user.id}")
            if new_filename:
                delete_old_image(user.foto_perfil)
                user.foto_perfil = new_filename
                request.session[SESSION_FOTO_PERFIL] = new_filename
        user.save()
        messages.success(request, "Perfil actualizado.")

    return render(request, "safezone_app/perfil.html", {'user': user})
