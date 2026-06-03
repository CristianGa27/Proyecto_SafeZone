"""
Constantes del sistema SafeZone.

Centraliza todos los valores que se repiten en el código
para evitar errores por typos y facilitar mantenimiento.
"""


class UserRole:
    """Roles disponibles en el sistema."""

    ADMIN_PRINCIPAL = 'admin_principal'
    ADMIN_TECNICO = 'admin_tecnico'
    ADMIN = 'admin'
    MODERADOR = 'moderador'
    USUARIO = 'usuario'
    GUEST = 'guest'
    USER = 'user'

    # Grupos de permisos
    ADMIN_ROLES = (ADMIN_PRINCIPAL, ADMIN, MODERADOR)
    ALL_ADMIN_ROLES = (ADMIN_PRINCIPAL, ADMIN_TECNICO, ADMIN)


class ReportStatus:
    """Estados posibles de un reporte."""

    NUEVO = 'nuevo'
    PENDIENTE = 'pendiente'
    APROBADO = 'aprobado'
    EN_PROGRESO = 'en_progreso'
    RESUELTO = 'resuelto'
    CERRADO = 'cerrado'
    RECHAZADO = 'rechazado'

    # Estados válidos para el flujo técnico
    TECHNICAL_FLOW = (PENDIENTE, EN_PROGRESO, RESUELTO, CERRADO)

    # Estados que se muestran en el panel técnico
    TECHNICAL_PANEL = (PENDIENTE, EN_PROGRESO, RESUELTO, CERRADO)


class SeverityLevel:
    """Niveles de gravedad de un reporte."""

    CRITICO = 'critico'
    SEVERO = 'severo'
    MODERADO = 'moderado'
    LEVE = 'leve'

    # Orden para consultas SQL
    ORDER = (CRITICO, SEVERO, MODERADO, LEVE)


# --- Configuración de archivos ---

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_REPORT_IMAGES = 3

# --- Claves de sesión ---

SESSION_USER_ID = 'user_id'
SESSION_USERNAME = 'username'
SESSION_USER_ROLE = 'user_role'
SESSION_FOTO_PERFIL = 'foto_perfil'
