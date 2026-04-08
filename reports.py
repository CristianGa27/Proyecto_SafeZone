# -*- coding: utf-8 -*-
import logging
import os

import mysql.connector
from flask import (Blueprint, flash, jsonify, redirect, render_template,
                   request, session, url_for)
from werkzeug.utils import secure_filename

from config import UPLOAD_FOLDER
from database import get_db

reports_bp = Blueprint('reports', __name__)


def _is_guest():
    return session.get('user_role') == 'guest' or session.get(
        'user_id') is None


@reports_bp.route("/inicio")
def inicio_html():
    if 'user_role' not in session:
        flash("Debes iniciar sesión para acceder.", 'error')
        return redirect(url_for("auth.login_html"))
    return render_template("inicio.html")


@reports_bp.route("/panel_info")
def panel_info_html():
    if session.get('user_role') not in ['admin_principal', 'admin']:
        flash("Acceso denegado.", 'error')
        return redirect(url_for("auth.login_html"))

    stats = {
        'reportes_totales': 0,
        'reparaciones': 0,
        'en_proceso': 0,
        'zona_critica': 'Sin datos',
        'reportes_mes': []}
    conn = get_db()
    if not conn:
        return render_template("panel_de_informacion.html", stats=stats)

    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT COUNT(*) as total,
                SUM(CASE WHEN estado = 'cerrado' THEN 1 ELSE 0 END) as cerrados,
                SUM(CASE WHEN estado IN ('en_progreso', 'pendiente') THEN 1 ELSE 0 END) as en_proceso
            FROM Reportes
        """)
        result = cursor.fetchone()
        if result:
            stats.update(
                {
                    'reportes_totales': result['total'],
                    'reparaciones': result['cerrados'],
                    'en_proceso': result['en_proceso']})

        cursor.execute(
            "SELECT barrio, COUNT(*) as total FROM Reportes WHERE barrio IS NOT NULL AND barrio != '' GROUP BY barrio ORDER BY total DESC LIMIT 1")
        result = cursor.fetchone()
        if result:
            stats['zona_critica'] = result['barrio']

        cursor.execute("""
            SELECT DATE_FORMAT(fecha_reporte, '%Y-%m') as mes, COUNT(*) as total
            FROM Reportes WHERE fecha_reporte >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
            GROUP BY DATE_FORMAT(fecha_reporte, '%Y-%m') ORDER BY mes DESC LIMIT 6
        """)
        reportes_mes = cursor.fetchall()
        if reportes_mes:
            max_r = max(r['total'] for r in reportes_mes)
            stats['reportes_mes'] = [{'mes': r['mes'], 'total': r['total'], 'height': max(
                int((r['total'] / max_r) * 100), 10)} for r in reversed(reportes_mes)]
    except Exception as e:
        logging.error(f"Error en panel_info: {e}", exc_info=True)
        flash(f"Error obteniendo estadísticas: {e}", 'error')
    finally:
        if cursor:
            cursor.close()
        if conn.is_connected():
            conn.close()

    return render_template("panel_de_informacion.html", stats=stats)


@reports_bp.route("/reporte")
def registro_html():
    if 'user_id' not in session or session.get('user_role') == 'guest':
        flash(
            "Debes iniciar sesión y completar tu perfil para poder reportar un daño vial.",
            'error')
        return redirect(url_for("auth.login_html"))

    conn = get_db()

    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT telefono, direccion_residencia, numero_documento FROM Usuarios WHERE id = %s",
            (session.get('user_id'),
             ))
        user_data = cursor.fetchone()
        if not user_data or not user_data.get('telefono') or not user_data.get(
                'direccion_residencia') or not user_data.get('numero_documento'):
            cursor.close()
            conn.close()
            flash("ACCESO BLOQUEADO: Tu perfil está Incompleto. Para seguir, debes registrar un celular, dirección de residencia y documento de identidad válidos para asegurar la identificación del ciudadano.", "warning")
            return redirect(url_for('auth.perfil'))
        cursor.close()

    zonas, tipos_anomalia = [], []
    if conn:
        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT nombre_zona, zona_geografica FROM Zonas WHERE activo = TRUE ORDER BY zona_geografica, nombre_zona")
            zonas = cursor.fetchall()
            cursor.execute(
                "SELECT id, nombre_anomalia FROM TiposAnomalia WHERE activo = TRUE ORDER BY nombre_anomalia")
            tipos_anomalia = cursor.fetchall()
        except Exception as e:
            logging.error(
                f"Error al cargar opciones de registro: {e}",
                exc_info=True)
        finally:
            if cursor:
                cursor.close()
            if conn.is_connected():
                conn.close()
    return render_template(
        'registro_deusuario.html',
        zonas=zonas,
        tipos_anomalia=tipos_anomalia)


@reports_bp.route("/mis_reportes")
def mis_reportes_html():
    if _is_guest():
        flash("Funcionalidad solo disponible para usuarios registrados.", 'error')
        return redirect(url_for("reports.registro_html"))

    conn = get_db()
    reportes = []
    if conn is None:
        flash("Error al conectar a la base de datos.", 'error')
        return render_template("mis_reportes.html", reportes=reportes)

    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT R.id, R.ubicacion, R.barrio as nombre_zona, T.nombre_anomalia, R.gravedad,
                R.descripcion, R.fecha_reporte, R.estado, R.observaciones,
                R.imagen, R.imagen2, R.imagen3, R.latitud, R.longitud
            FROM Reportes R
            LEFT JOIN TiposAnomalia T ON R.id_tipo_anomalia = T.id
            WHERE R.usuario_id = %s ORDER BY R.id DESC
        """, (session['user_id'],))
        reportes = cursor.fetchall()
    except Exception as e:
        logging.error(f"Error en mis_reportes: {e}", exc_info=True)
        flash("Error al cargar tus reportes.", 'error')
    finally:
        if cursor:
            cursor.close()
        if conn.is_connected():
            conn.close()

    return render_template("mis_reportes.html", reportes=reportes)


@reports_bp.route("/registro", methods=["POST"])
def registro():
    conn = get_db()
    if conn is None:
        flash("Error de conexión. Reporte no guardado.", 'error')
        return redirect(url_for("reports.registro_html"))

    ubicacion = request.form.get("location")
    barrio = request.form.get("zone_id")
    tipo_anomalia_id = request.form.get("tipo_anomalia_id")
    gravedad = request.form.get("severity")
    descripcion = request.form.get("description")
    info_adicional = request.form.get("additionalInfo")

    for campo, msg in [(ubicacion, "ubicación"), (barrio, "barrio"), (tipo_anomalia_id,
                                                                      "tipo de anomalía"), (gravedad, "gravedad"), (descripcion, "descripción")]:
        if not campo:
            flash(f"El campo {msg} es requerido.", 'error')
            return redirect(url_for("reports.registro_html"))

    try:
        latitud = float(request.form.get("latitude") or 0) or None
        longitud = float(request.form.get("longitude") or 0) or None
    except (ValueError, TypeError):
        latitud, longitud = None, None

    imagenes = [None, None, None]
    if 'imageUpload' in request.files:
        for i, file in enumerate(request.files.getlist('imageUpload')[:3]):
            if file and file.filename:
                filename = f"{
                    os.urandom(8).hex()}_{
                    secure_filename(
                        file.filename)}"
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                imagenes[i] = filename

    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Reportes (ubicacion, barrio, id_tipo_anomalia, gravedad, descripcion,
                info_adicional, imagen, imagen2, imagen3, usuario_id, estado, latitud, longitud)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'nuevo', %s, %s)
        """, (ubicacion, barrio, int(tipo_anomalia_id), gravedad, descripcion,
              info_adicional, imagenes[0], imagenes[1], imagenes[2],
              session.get('user_id'), latitud, longitud))
        conn.commit()
        flash(
            "Reporte enviado exitosamente. ¡Gracias por tu colaboración!",
            'success')
    except mysql.connector.Error as e:
        logging.error(f"Error al crear reporte: {e}", exc_info=True)
        conn.rollback()
        flash("Error al guardar el reporte.", 'error')
    finally:
        if cursor:
            cursor.close()
        if conn.is_connected():
            conn.close()

    return redirect(url_for("reports.registro_html"))


@reports_bp.route("/api/reportes")
def api_reportes():
    if 'user_role' not in session:
        return jsonify({"error": "No autorizado"}), 401

    conn = get_db()
    if not conn:
        return jsonify({"error": "Error de conexión"}), 500

    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT R.id, R.ubicacion, R.barrio as zona, T.nombre_anomalia as tipo_anomalia,
                R.gravedad, R.descripcion, R.info_adicional, R.fecha_reporte, R.estado,
                R.latitud as lat, R.longitud as lng, R.imagen, R.imagen2, R.imagen3,
                U.nombre_usuario AS reportado_por
            FROM Reportes R
            LEFT JOIN Usuarios U ON R.usuario_id = U.id
            LEFT JOIN TiposAnomalia T ON R.id_tipo_anomalia = T.id
            ORDER BY R.fecha_reporte DESC
        """)
        reportes = cursor.fetchall()
        for r in reportes:
            if r['fecha_reporte']:
                r['fecha_reporte'] = r['fecha_reporte'].strftime(
                    '%Y-%m-%d %H:%M:%S')
            for i, field in enumerate(['imagen', 'imagen2', 'imagen3'], 1):
                key = 'image_url' if i == 1 else f'image_url{i}'
                r[key] = f"/static/uploads/{r[field]}" if r[field] else None
        return jsonify(reportes)
    except mysql.connector.Error as e:
        logging.error(f"Error en api_reportes: {e}", exc_info=True)
        return jsonify({"error": "Error al obtener reportes"}), 500
    finally:
        if cursor:
            cursor.close()
        if conn.is_connected():
            conn.close()


@reports_bp.route("/editar_reporte/<int:reporte_id>")
def editar_reporte_html(reporte_id):
    if _is_guest():
        flash("Funcionalidad solo disponible para usuarios registrados.", 'error')
        return redirect(url_for("reports.registro_html"))

    conn = get_db()
    if conn is None:
        flash("Error de conexión.", 'error')
        return redirect(url_for("reports.mis_reportes_html"))

    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT R.*, T.nombre_anomalia FROM Reportes R
            LEFT JOIN TiposAnomalia T ON R.id_tipo_anomalia = T.id
            WHERE R.id = %s AND R.usuario_id = %s
        """, (reporte_id, session['user_id']))
        reporte = cursor.fetchone()

        if not reporte:
            flash("Reporte no encontrado o sin permisos.", 'error')
            return redirect(url_for("reports.mis_reportes_html"))

        cursor.execute(
            "SELECT id, nombre_anomalia FROM TiposAnomalia ORDER BY nombre_anomalia")
        tipos_anomalia = cursor.fetchall()
        cursor.execute(
            "SELECT nombre_zona, zona_geografica FROM Zonas WHERE activo = TRUE ORDER BY zona_geografica, nombre_zona")
        zonas = cursor.fetchall()

        return render_template(
            "editar_reporte.html",
            reporte=reporte,
            tipos_anomalia=tipos_anomalia,
            zonas=zonas)
    except Exception as e:
        logging.error(
            f"Error en cargar reporte para editar: {e}",
            exc_info=True)
        flash("Error al cargar el reporte.", 'error')
        return redirect(url_for("reports.mis_reportes_html"))
    finally:
        if cursor:
            cursor.close()
        if conn.is_connected():
            conn.close()


@reports_bp.route("/actualizar_reporte/<int:reporte_id>", methods=["POST"])
def actualizar_reporte(reporte_id):
    if _is_guest():
        flash("Funcionalidad solo disponible para usuarios registrados.", 'error')
        return redirect(url_for("reports.registro_html"))

    conn = get_db()
    if conn is None:
        flash("Error de conexión.", 'error')
        return redirect(url_for("reports.mis_reportes_html"))

    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM Reportes WHERE id = %s AND usuario_id = %s",
            (reporte_id,
             session['user_id']))
        if not cursor.fetchone():
            flash("Reporte no encontrado o sin permisos.", 'error')
            return redirect(url_for("reports.mis_reportes_html"))

        ubicacion = request.form.get("location")
        barrio = request.form.get("zone_id")
        tipo_anomalia_id = request.form.get("tipo_anomalia_id")
        gravedad = request.form.get("severity")
        descripcion = request.form.get("description")
        info_adicional = request.form.get("additionalInfo")

        if not all([ubicacion,
                    barrio,
                    tipo_anomalia_id,
                    gravedad,
                    descripcion]):
            flash("Todos los campos obligatorios deben estar completos.", 'error')
            return redirect(
                url_for(
                    "reports.editar_reporte_html",
                    reporte_id=reporte_id))

        cursor.execute("""
            UPDATE Reportes SET ubicacion=%s, barrio=%s, id_tipo_anomalia=%s,
                gravedad=%s, descripcion=%s, info_adicional=%s
            WHERE id=%s AND usuario_id=%s
        """, (ubicacion, barrio, int(tipo_anomalia_id), gravedad, descripcion,
              info_adicional, reporte_id, session['user_id']))
        conn.commit()
        flash("Reporte actualizado exitosamente.", 'success')
        return redirect(url_for("reports.mis_reportes_html"))
    except Exception as e:
        logging.error(
            f"Error al actualizar reporte {reporte_id}: {e}",
            exc_info=True)
        conn.rollback()
        flash("Error al actualizar el reporte.", 'error')
        return redirect(
            url_for(
                "reports.editar_reporte_html",
                reporte_id=reporte_id))
    finally:
        if cursor:
            cursor.close()
        if conn.is_connected():
            conn.close()
