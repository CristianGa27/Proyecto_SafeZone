from .auth import login_view, register_page, register, guest_login, logout_view, perfil, esperando_verificacion, verificar_token, solicitar_recuperacion, restablecer_contrasena
from .reports import inicio_html, registro_html, registro_reporte, mis_reportes_html, editar_reporte_html, actualizar_reporte
from .admin import panel_admin, panel_tecnico, validar, panel_info_html, admin_info, gestion_usuarios
from .api import api_reportes, api_estadisticas, mapa_html, estadisticas_html

__all__ = [
    'login_view', 'register_page', 'register', 'guest_login', 'logout_view', 'perfil', 'esperando_verificacion', 'verificar_token',
    'solicitar_recuperacion', 'restablecer_contrasena',
    'inicio_html', 'registro_html', 'registro_reporte', 'mis_reportes_html', 'editar_reporte_html', 'actualizar_reporte',
    'panel_admin', 'panel_tecnico', 'validar', 'panel_info_html', 'admin_info', 'gestion_usuarios',
    'api_reportes', 'api_estadisticas', 'mapa_html', 'estadisticas_html',
]
