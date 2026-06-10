"""
Formularios Django para SafeZone.

Centraliza la validación de datos que antes estaba dispersa
en las vistas, proporcionando validación declarativa y reutilizable.
"""

from django import forms

from .constants import ALLOWED_IMAGE_EXTENSIONS
from .models import Usuarios


# --- Autenticación ---

class LoginForm(forms.Form):
    """Formulario de inicio de sesión."""

    email = forms.EmailField(
        max_length=150,
        error_messages={'required': 'El correo es obligatorio.'}
    )
    password = forms.CharField(
        max_length=255,
        error_messages={'required': 'La contraseña es obligatoria.'}
    )


class RegisterForm(forms.Form):
    """Formulario de registro de nuevo usuario."""

    nombres = forms.CharField(
        max_length=50,
        min_length=2,
        error_messages={
            'required': 'Los nombres son obligatorios.',
            'min_length': 'El nombre debe tener al menos 2 caracteres.',
            'max_length': 'El nombre no puede superar los 50 caracteres.',
        }
    )
    apellidos = forms.CharField(
        max_length=50,
        min_length=2,
        error_messages={
            'required': 'Los apellidos son obligatorios.',
            'min_length': 'El apellido debe tener al menos 2 caracteres.',
            'max_length': 'El apellido no puede superar los 50 caracteres.',
        }
    )
    telefono = forms.CharField(
        max_length=20,
        error_messages={'required': 'El teléfono es obligatorio.'}
    )
    email = forms.EmailField(
        max_length=150,
        error_messages={
            'required': 'El correo electrónico es obligatorio.',
            'invalid': 'Ingresa un correo electrónico válido.',
        }
    )
    password = forms.CharField(
        min_length=6,
        max_length=255,
        error_messages={
            'required': 'La contraseña es obligatoria.',
            'min_length': 'La contraseña debe tener al menos 6 caracteres.',
        }
    )

    def clean_nombres(self):
        """Valida que los nombres solo contengan letras y espacios."""
        import re
        nombres = self.cleaned_data.get('nombres', '').strip()
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ ]+$', nombres):
            raise forms.ValidationError(
                'El nombre solo puede contener letras y espacios.'
            )
        return nombres

    def clean_apellidos(self):
        """Valida que los apellidos solo contengan letras y espacios."""
        import re
        apellidos = self.cleaned_data.get('apellidos', '').strip()
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ ]+$', apellidos):
            raise forms.ValidationError(
                'El apellido solo puede contener letras y espacios.'
            )
        return apellidos

    def clean_email(self):
        """Verifica que el correo no esté ya registrado."""
        email = self.cleaned_data.get('email', '').strip()
        if Usuarios.objects.filter(correo_electronico=email).exists():
            raise forms.ValidationError(
                "El correo electrónico ya está registrado."
            )
        return email

    def get_nombre_usuario(self):
        """Genera el nombre de usuario a partir de nombres y apellidos."""
        nombres = self.cleaned_data.get('nombres', '').strip()
        apellidos = self.cleaned_data.get('apellidos', '').strip()
        return f"{nombres} {apellidos}".strip()


# --- Perfil ---

class ProfileForm(forms.Form):
    """Formulario de actualización de perfil."""

    telefono = forms.CharField(max_length=20, required=False)
    direccion_residencia = forms.CharField(max_length=200, required=False)
    numero_documento = forms.CharField(max_length=50, required=False)
    foto_perfil = forms.ImageField(required=False)

    def clean_foto_perfil(self):
        """Valida la extensión del archivo de imagen."""
        foto = self.cleaned_data.get('foto_perfil')
        if foto:
            ext = foto.name.rsplit('.', 1)[-1].lower() if '.' in foto.name else ''
            if ext not in ALLOWED_IMAGE_EXTENSIONS:
                raise forms.ValidationError(
                    f"Formato no permitido. Usa: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}"
                )
        return foto


# --- Reportes ---

class ReportForm(forms.Form):
    """Formulario para crear un nuevo reporte de anomalía vial."""

    location = forms.CharField(max_length=500)
    zone_id = forms.CharField(max_length=100)
    tipo_anomalia_id = forms.IntegerField()
    severity = forms.CharField(max_length=8)
    description = forms.CharField()
    additional_info = forms.CharField(required=False)
    latitude = forms.FloatField(required=False)
    longitude = forms.FloatField(required=False)


class ReportUpdateForm(forms.Form):
    """Formulario para editar un reporte existente."""

    location = forms.CharField(max_length=500)
    zone_id = forms.CharField(max_length=100)
    tipo_anomalia_id = forms.IntegerField()
    severity = forms.CharField(max_length=8)
    description = forms.CharField()
    additional_info = forms.CharField(required=False)


class ReportValidationForm(forms.Form):
    """Formulario para que admins validen/cambien estado de un reporte."""

    estado = forms.CharField(max_length=11)
    observaciones = forms.CharField(required=False)
