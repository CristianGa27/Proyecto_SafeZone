"""
Decoradores de autenticación para SafeZone.

Reemplazan las verificaciones manuales repetidas en cada vista
con decoradores reutilizables y consistentes.
"""

from functools import wraps
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib import messages
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache

from .constants import UserRole, SESSION_USER_ID, SESSION_USER_ROLE


def login_required_safezone(view_func):
    """
    Requiere que el usuario tenga una sesión activa (no invitado).

    Redirige a login si no hay sesión, o si el usuario es invitado.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user_role = request.session.get(SESSION_USER_ROLE)
        user_id = request.session.get(SESSION_USER_ID)

        if user_role == UserRole.GUEST or not user_id:
            messages.error(
                request,
                "Debes iniciar sesión con tu cuenta para acceder."
            )
            return redirect('login_html')

        return view_func(request, *args, **kwargs)

    return never_cache(wrapper)


def session_required(view_func):
    """
    Requiere cualquier tipo de sesión (incluido invitado).

    Solo verifica que exista un user_role en la sesión.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if SESSION_USER_ROLE not in request.session:
            messages.error(request, "Debes iniciar sesión para acceder.")
            return redirect('login_html')

        return view_func(request, *args, **kwargs)

    return never_cache(wrapper)


def admin_required(view_func):
    """
    Requiere rol de administrador principal, admin genérico o moderador.

    Para acceso a paneles de administración y gestión de usuarios.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user_role = request.session.get(SESSION_USER_ROLE)

        if user_role not in UserRole.ADMIN_ROLES:
            messages.error(
                request,
                "Acceso denegado. Se requiere perfil administrativo."
            )
            return redirect('login_html')

        return view_func(request, *args, **kwargs)

    return never_cache(wrapper)


def admin_or_tecnico_required(view_func):
    """
    Requiere rol de administrador (cualquier tipo) o técnico.

    Para acciones de validación de reportes.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user_role = request.session.get(SESSION_USER_ROLE)

        if user_role not in UserRole.ALL_ADMIN_ROLES:
            messages.error(request, "Acceso denegado.")
            return redirect('login_html')

        return view_func(request, *args, **kwargs)

    return never_cache(wrapper)


def tecnico_required(view_func):
    """Requiere rol de administrador técnico."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.session.get(SESSION_USER_ROLE) != UserRole.ADMIN_TECNICO:
            messages.error(request, "Acceso denegado.")
            return redirect('login_html')

        return view_func(request, *args, **kwargs)

    return never_cache(wrapper)

def verificar_url_segura(view_func):
    """
    Verifica que las redirecciones en parámetros 'next' apunten
    estrictamente al dominio seguro de la aplicación.
    Evita ataques de Open Redirect.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Captura cualquier parámetro 'next' si intentan forzar una redirección
        next_url = request.GET.get('next') or request.POST.get('next')
        
        if next_url:
            # ESCUDO: Valida que la URL apunte estrictamente a nuestro dominio
            is_safe = url_has_allowed_host_and_scheme(
                url=next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure()
            )
            # Si intentan redirigir a un sitio externo malicioso, los mandamos a la página de inicio
            if not is_safe:
                return redirect('inicio_html')
                
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def no_cache_required(view_func):
    """
    Añade cabeceras HTTP a la respuesta para destruir la caché por completo,
    asegurando que los datos no se queden cacheados en el navegador del usuario.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        # Añade cabeceras HTTP para destruir la caché por completo
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    return _wrapped_view