import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'safezone_project.settings')
django.setup()

from django.db import connection

def check_tables():
    with connection.cursor() as cursor:
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        print("Tablas en la base de datos:")
        for table in tables:
            print(table[0])
            
        # Intentar forzar la eliminación de la tabla Nueva (ignorando mayúsculas/minúsculas)
        try:
            cursor.execute("DROP TABLE IF EXISTS nueva;")
            cursor.execute("DROP TABLE IF EXISTS Nueva;")
            print("\nIntenté borrar 'Nueva' de nuevo.")
        except Exception as e:
            print(f"Error borrando: {e}")

        print("\nTablas después del borrado:")
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        for table in tables:
            print(table[0])

if __name__ == '__main__':
    check_tables()
