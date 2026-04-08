# SafeZone - Sistema de Reportes de Anomalías Viales

**Sistema completo para reportar y gestionar baches y vías dañadas**

## ✅ Estado del Proyecto: LISTO PARA PRODUCCIÓN

### 🚀 Características Principales
- **2 tipos de anomalías:** Baches y Vías Dañadas
- **114 barrios** organizados por zonas geográficas
- **Codificación UTF-8** completa para caracteres especiales
- **Sistema dual de administración:** Principal y Técnico
- **Panel de información** con estadísticas en tiempo real
- **Mapa interactivo** con geolocalización
- **Interfaz responsive** y profesional

## 📊 Base de Datos
- **Nombre:** Prueba
- **Codificación:** UTF-8 (utf8mb4)
- **Usuarios:** 4 (Admin Principal, Admin Técnico, Usuario, Invitado)
- **Barrios:** 114 organizados por 11 zonas geográficas
- **Estados de reportes:** pendiente, aprobado, en_proceso, resuelto, cerrado, rechazado

## 👥 Usuarios del Sistema
- **admin@safezone.com** - Administrador Principal
- **tecnico@safezone.com** - Administrador Técnico
- **Usuarios regulares** - Pueden crear y gestionar reportes
- **Invitados** - Acceso básico para reportes

## 🗂️ Estructura del Proyecto

El proyecto ha sido reorganizado en módulos separados para mejor mantenibilidad:

### Archivos principales:

- **`app.py`** - Aplicación Flask principal (simplificada)
- **`config.py`** - Configuraciones y constantes
- **`database.py`** - Conexión y operaciones de base de datos
- **`auth.py`** - Rutas de autenticación (login, registro, logout)
- **`reports.py`** - Rutas relacionadas con reportes
- **`admin.py`** - Rutas de administración
- **`visualizations.py`** - Rutas de mapa y estadísticas
- **`utils.py`** - Funciones auxiliares
- **`requirements.txt`** - Dependencias del proyecto

### Estructura de carpetas:
```
├── app.py                 # Aplicación principal
├── config.py             # Configuraciones
├── database.py           # Operaciones de BD
├── auth.py               # Autenticación
├── reports.py            # Gestión de reportes
├── admin.py              # Panel de administración
├── visualizations.py     # Mapa y estadísticas
├── utils.py              # Utilidades
├── requirements.txt      # Dependencias
├── static/               # Archivos estáticos
│   ├── CSS/             # Estilos
│   ├── js/              # JavaScript
│   ├── img/             # Imágenes
│   └── uploads/         # Archivos subidos
└── templates/           # Plantillas HTML
```

## Instalación

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Configurar la base de datos en `config.py`:
```python
DB_CONFIG = {
    'host': "localhost",
    'user': "root",
    'password': "tu_password",  # Cambiar aquí
    'database': "Prueba",
    'port': 3306
}
```

3. Ejecutar la aplicación:
```bash
python app.py
```

## Nuevas funcionalidades agregadas:

### Mapa Interactivo
- Visualización de reportes en mapa con coordenadas
- Filtros por gravedad (crítico, severo, moderado, leve)
- API endpoint para datos en tiempo real
- Acceso desde: `/mapa`

### Estadísticas
- Dashboard con métricas del sistema
- Reportes por estado, gravedad, zona y tipo
- Gráficos de tendencias mensuales
- API endpoint para datos estadísticos
- Acceso desde: `/estadisticas`

## Beneficios de la nueva estructura:

- **Separación de responsabilidades**: Cada módulo tiene una función específica
- **Mantenibilidad**: Más fácil encontrar y modificar código
- **Escalabilidad**: Fácil agregar nuevas funcionalidades
- **Reutilización**: Funciones de BD y utilidades pueden reutilizarse
- **Testing**: Cada módulo puede probarse independientemente
- **Navegación mejorada**: Enlaces consistentes a mapa y estadísticas en todos los paneles
- **Diseño profesional**: Interfaz unificada con marca SafeZone consistente

## 🎯 Instalación y Configuración

### Requisitos
- Python 3.8+
- MySQL 8.0+
- Navegador web moderno

### Instalación
1. **Clonar el repositorio**
2. **Instalar dependencias:** `pip install -r requirements.txt`
3. **Configurar base de datos:** Ejecutar `create_database_updated.sql`
4. **Configurar config.py** con tus credenciales de MySQL
5. **Ejecutar:** `python app.py`

### Acceso al Sistema
- **URL:** http://localhost:5000
- **Admin Principal:** admin@safezone.com
- **Admin Técnico:** tecnico@safezone.com

## 🧹 Limpieza del Proyecto (Diciembre 2024):

### ✅ Archivos Eliminados
- **PROYECTO_COMPLETADO.md** - Documentación temporal innecesaria
- **__pycache__/** - Archivos compilados de Python (se regeneran automáticamente)
- **.vscode/settings.json** - Configuración vacía de VSCode
- **Imágenes duplicadas** - Eliminadas imágenes de prueba y duplicadas en uploads/

### 🔧 Código Optimizado
- **Espacios en blanco** eliminados en database.py
- **Imports verificados** - todos los imports son necesarios
- **Funciones consolidadas** - sin código duplicado
- **.gitignore agregado** - para evitar archivos innecesarios en el futuro

### 🎨 Interfaz Mejorada con Tema Oscuro
- Fondo cambiado de blanco a tonos oscuros para mejor experiencia visual
- Tabla de reportes con fondo oscuro (#111827) y mejor contraste
- Botones de acción con efectos hover y gradientes
- Formulario de edición con diseño moderno y oscuro
- Mejores efectos visuales y transiciones

### 🛡️ Seguridad Mejorada
- Verificación de propiedad del reporte antes de permitir edición
- Validación de campos obligatorios en la edición
- Protección contra usuarios no autenticados
- Solo el usuario propietario puede editar sus reportes

## Configuración adicional:

- Cambiar `SECRET_KEY` en `config.py`
- Ajustar configuración de base de datos según tu entorno