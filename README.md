# SafeZone - Sistema de Reportes de Anomalías Viales

**Sistema completo para reportar y gestionar baches y vías dañadas - Ahora en Django**

## ✅ Estado del Proyecto: MIGRADO A DJANGO

### 🚀 Características Principales
- **2 tipos de anomalías:** Baches y Vías Dañadas
- **114 barrios** organizados por zonas geográficas
- **Codificación UTF-8** completa para caracteres especiales
- **Sistema dual de administración:** Principal y Técnico
- **Panel de información** con estadísticas en tiempo real
- **Mapa interactivo** con geolocalización
- **Interfaz responsive** y profesional
- **Migración Exitosa:** Todo el sistema ahora corre sobre Django 6.0

## 📊 Base de Datos
- **Nombre:** Prueba (MySQL)
- **Codificación:** UTF-8 (utf8mb4)
- **Usuarios:** 4 (Admin Principal, Admin Técnico, Usuario, Invitado)
- **Barrios:** 114 organizados por 11 zonas geográficas
- **Estados de reportes:** pendiente, aprobado, en_proceso, resuelto, cerrado, rechazado

## 👥 Usuarios del Sistema
- **admin@safezone.com** - Administrador Principal
- **tecnico@safezone.com** - Administrador Técnico
- **Usuarios regulares** - Pueden crear y gestionar reportes
- **Invitados** - Acceso básico para reportes

## 🗂️ Estructura del Proyecto (Django)

El proyecto ha sido migrado de Flask a Django para mejorar la escalabilidad y seguridad.

### Estructura de carpetas:
```
├── manage.py                # Punto de entrada de Django
├── safezone_project/        # Configuración del proyecto (settings.py, urls.py)
├── safezone_app/            # Aplicación principal (models.py, views.py, urls.py)
├── requirements.txt         # Dependencias actualizadas
├── .env                     # Variables de entorno
├── static/                  # Archivos estáticos
│   ├── CSS/                # Estilos
│   ├── js/                 # JavaScript
│   ├── img/                # Imágenes
│   └── uploads/            # Archivos subidos
└── templates/               # Plantillas HTML migradas a Django syntax
```

## 🎯 Instalación y Configuración

### Requisitos
- Python 3.8+
- MySQL 8.0+
- Navegador web moderno

### Instalación
1. **Clonar el repositorio**
2. **Instalar dependencias:** `pip install -r requirements.txt`
3. **Configurar base de datos:** Asegúrate de tener la base de datos `Prueba` creada (puedes usar `prueba.sql`).
4. **Configurar .env** con tus credenciales de MySQL:
   ```env
   DB_HOST=localhost
   DB_NAME=Prueba
   DB_USER=root
   DB_PASSWORD=tu_password
   SECRET_KEY=tu_secreto
   ```
5. **Ejecutar servidor:**
   ```bash
   python manage.py runserver
   ```

## 🚀 Acceso al Sistema
- **URL:** http://localhost:8000
- **Admin Principal:** admin@safezone.com
- **Admin Técnico:** tecnico@safezone.com

## 🧹 Migración de Flask a Django (Mayo 2026):
- Se eliminaron todos los archivos relacionados con Flask (`app.py`, `auth.py`, `reports.py`, etc.).
- Se implementaron los modelos en Django usando `managed = False` para respetar la base de datos existente.
- Se adaptaron las vistas de Flask a la arquitectura de Django.
- Se convirtieron las plantillas Jinja2 a la sintaxis nativa de Django.
- Se configuró el sistema de autenticación para que reconozca los hashes de `bcrypt` existentes.

## 🛡️ Seguridad Mejorada
- Verificación de propiedad del reporte antes de permitir edición.
- Protección contra usuarios no autenticados mediante el sistema de sesiones de Django.
- Sistema de validación de formularios robusto.