import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'safezone_project.settings')
django.setup()

from django.db import connection

def clean_database():
    with connection.cursor() as cursor:
        try:
            print("Eliminando la tabla 'Nueva' que no sirve...")
            cursor.execute("DROP TABLE IF EXISTS Nueva;")
            print("Tabla 'Nueva' eliminada.")
        except Exception as e:
            print(f"Error al eliminar 'Nueva': {e}")
        
        try:
            print("Limpiando sesiones antiguas...")
            cursor.execute("DELETE FROM django_session WHERE expire_date < NOW();")
            print("Sesiones expiradas eliminadas.")
        except Exception as e:
            print(f"Error limpiando sesiones: {e}")

if __name__ == '__main__':
    clean_database()
