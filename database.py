# -*- coding: utf-8 -*-
import mysql.connector

from config import DB_CONFIG


def get_db():
    """Establece conexión a la base de datos."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute("SET NAMES utf8mb4")
        cursor.close()
        return conn
    except mysql.connector.Error:
        return None


def get_user_by_email_with_role(email):
    """Obtiene un usuario por email incluyendo su rol."""
    return execute_query(
        """
        SELECT u.id, u.nombre_usuario, u.contrasena_hash, u.id_rol, r.nombre_rol, u.foto_perfil
        FROM Usuarios u
        LEFT JOIN Roles r ON u.id_rol = r.id
        WHERE u.correo_electronico = %s
        """,
        (email,),
        fetch_one=True,
    )


def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    """Ejecuta una consulta de forma segura y retorna el resultado."""
    conn = get_db()
    if not conn:
        return None
    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        if fetch_one:
            return cursor.fetchone()
        if fetch_all:
            return cursor.fetchall()
        return cursor.rowcount
    except mysql.connector.Error:
        return None
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
