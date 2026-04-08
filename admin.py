# -*- coding: utf-8 -*-
import mysql.connector
from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)

from database import execute_query

admin_bp = Blueprint('admin', __name__)


@admin_bp.route("/admin_panel")
def panel_admin():
    if session.get('user_role') not in ['admin_principal', 'admin', 'moderador']:
        flash("Acceso denegado.", 'error')
        return redirect(url_for("auth.login_html"))

    reportes = execute_query("""
        SELECT R.id, U.nombre_usuario AS reportado_por, R.ubicacion, R.barrio as nombre_zona,
            T.nombre_anomalia, R.gravedad, R.descripcion, R.fecha_reporte,
            R.estado, R.observaciones, R.imagen, R.latitud, R.longitud
        FROM Reportes R
        LEFT JOIN Usuarios U ON R.usuario_id = U.id
        LEFT JOIN TiposAnomalia T ON R.id_tipo_anomalia = T.id
        ORDER BY R.id DESC
    """, fetch_all=True)

    if reportes is None:
        flash("Error de conexión o al cargar los reportes.", 'error')
        reportes = []

    return render_template("validacion_reporte.html", reportes=reportes)


@admin_bp.route("/panel_tecnico")
def panel_tecnico():
    if session.get('user_role') != 'admin_tecnico':
        flash("Acceso denegado.", 'error')
        return redirect(url_for("auth.login_html"))

    reportes = execute_query("""
        SELECT R.id, U.nombre_usuario AS reportado_por, R.ubicacion, R.barrio as zona,
            T.nombre_anomalia, R.gravedad, R.descripcion, R.fecha_reporte,
            R.estado, R.observaciones, R.imagen, R.latitud, R.longitud, R.info_adicional
        FROM Reportes R
        LEFT JOIN Usuarios U ON R.usuario_id = U.id
        LEFT JOIN TiposAnomalia T ON R.id_tipo_anomalia = T.id
        WHERE R.estado IN ('pendiente', 'en_progreso', 'resuelto', 'cerrado')
        ORDER BY CASE R.estado
            WHEN 'pendiente' THEN 1 WHEN 'en_progreso' THEN 2
            WHEN 'resuelto' THEN 3 WHEN 'cerrado' THEN 4
        END, R.fecha_reporte DESC
    """, fetch_all=True)

    if reportes is None:
        flash("Error de conexión o al cargar los reportes.", 'error')
        reportes = []

    return render_template("panel_tecnico.html", reportes=reportes)


@admin_bp.route("/validar/<int:id>", methods=["POST"])
def validar(id):
    user_role = session.get('user_role')
    if user_role not in ['admin_principal', 'admin_tecnico', 'admin']:
        flash("Acceso denegado.", 'error')
        return redirect(url_for("auth.login_html"))

    estado = request.form.get("estado")
    observaciones = request.form.get("observaciones")

    if user_role == 'admin_tecnico' and estado not in [
            'pendiente', 'en_progreso', 'resuelto', 'cerrado']:
        flash("Estado no válido para el flujo técnico.", 'error')
        return redirect(url_for("admin.panel_tecnico"))

    result = execute_query(
        "UPDATE Reportes SET estado=%s, observaciones=%s WHERE id=%s",
        (estado, observaciones, id)
    )

    if result is not None:
        flash("Validación guardada correctamente.", 'success')
    else:
        flash("Error de conexión o al validar el reporte.", 'error')

    return redirect(url_for("admin.panel_tecnico" if user_role ==
                    'admin_tecnico' else "admin.panel_admin"))


@admin_bp.route("/admin_info")
def admin_info():
    if session.get('user_role') not in ['admin_principal', 'admin', 'moderador']:
        flash("Acceso denegado.", 'error')
        return redirect(url_for("auth.login_html"))
    return render_template("panel_de_informacion.html")


@admin_bp.route("/usuarios")
def gestion_usuarios():
    if session.get('user_role') not in ['admin_principal', 'moderador']:
        flash("Acceso denegado. Solo Súper Administradores o Moderadores pueden ver esta sección.", 'error')
        return redirect(url_for("auth.login_html"))

    # Consultar usuarios de la base de datos (excluyendo contraseñas y otros roles)
    usuarios = execute_query("""
        SELECT u.id, u.nombre_usuario, u.correo_electronico, u.telefono,
               u.direccion_residencia, u.numero_documento, u.estado_cuenta,
               u.fecha_registro, r.nombre_rol, u.verificado
        FROM Usuarios u
        LEFT JOIN Roles r ON u.id_rol = r.id
        WHERE r.nombre_rol = 'usuario'
        ORDER BY u.fecha_registro DESC
    """, fetch_all=True)

    if usuarios is None:
        flash("Error de conexión o al cargar los usuarios.", 'error')
        usuarios = []

    # Calcular completitud para la vista
    for u in usuarios:
        campos_perfil = [u.get('telefono'), u.get('direccion_residencia'), u.get('numero_documento')]
        campos_completos = sum(1 for c in campos_perfil if c and str(c).strip())
        u['completitud'] = int((campos_completos / 3) * 100)
        
        faltantes = []
        if not u.get('telefono'): faltantes.append('Teléfono')
        if not u.get('direccion_residencia'): faltantes.append('Dirección')
        if not u.get('numero_documento'): faltantes.append('Documento')
        u['faltantes'] = ", ".join(faltantes) if faltantes else "Completo"

    return render_template("gestion_usuarios.html", usuarios=usuarios)

