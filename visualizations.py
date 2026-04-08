# -*- coding: utf-8 -*-
import calendar

from flask import (Blueprint, flash, jsonify, redirect, render_template,
                   request, session, url_for)

from database import execute_query

visualizations_bp = Blueprint('visualizations', __name__)


@visualizations_bp.route("/mapa")
def mapa_html():
    if 'user_role' not in session:
        flash("Debes iniciar sesión para acceder.", 'error')
        return redirect(url_for("auth.login_html"))
    return render_template("mapa.html")


@visualizations_bp.route("/estadisticas")
def estadisticas_html():
    if 'user_role' not in session:
        flash("Debes iniciar sesión para acceder.", 'error')
        return redirect(url_for("auth.login_html"))
    return render_template("estadisticas.html")


@visualizations_bp.route("/api/estadisticas")
def api_estadisticas():
    if 'user_role' not in session:
        return jsonify({"error": "No autorizado"}), 401
    return jsonify(get_estadisticas_sistema())


@visualizations_bp.route("/api/reportes")
def api_reportes():
    if 'user_role' not in session:
        return jsonify({"error": "No autorizado"}), 401

    estado_filtro = request.args.get('estado', 'todos')
    is_admin = session.get('user_role') in [
        'admin_principal', 'admin_tecnico', 'admin']

    base_query = """
        SELECT r.id, r.ubicacion, r.barrio as zona, r.gravedad, r.descripcion, r.info_adicional,
            r.imagen, r.imagen2, r.imagen3, r.latitud as lat, r.longitud as lng,
            r.estado, r.fecha_reporte, ta.nombre_anomalia as tipo_anomalia
        FROM Reportes r
        LEFT JOIN TiposAnomalia ta ON r.id_tipo_anomalia = ta.id
    """

    if estado_filtro == 'todos':
        query = base_query if is_admin else base_query + \
            " WHERE r.estado IN ('pendiente', 'en_progreso', 'resuelto', 'cerrado')"
        params = ()
    elif estado_filtro in ['pendiente', 'en_progreso', 'resuelto', 'cerrado', 'rechazado']:
        query = base_query + " WHERE r.estado = %s"
        params = (estado_filtro,)
    else:
        return jsonify({"error": "Estado de filtro inválido"}), 400

    query += " ORDER BY r.fecha_reporte DESC"
    reportes = execute_query(query, params, fetch_all=True)

    if reportes is None:
        return jsonify({"error": "Error de conexión"}), 500

    for r in reportes:
        for i, field in enumerate(['imagen', 'imagen2', 'imagen3'], 1):
            key = 'image_url' if i == 1 else f'image_url{i}'
            r[key] = f"/static/uploads/{r[field]}" if r[field] else None
        if r['fecha_reporte']:
            r['fecha_reporte'] = r['fecha_reporte'].strftime(
                '%Y-%m-%d %H:%M:%S')

    return jsonify(reportes)


def get_estadisticas_sistema():
    stats = {
        'reportes_mes': [{'mes': 'Nov 2024', 'total': 2}, {'mes': 'Dic 2024', 'total': 3}],
        'severidad': [
            {'gravedad': 'critico', 'total': 1}, {'gravedad': 'severo', 'total': 2},
            {'gravedad': 'moderado', 'total': 1}, {'gravedad': 'leve', 'total': 1}
        ],
        'evolucion': [{'semana': i, 'total': t} for i, t in enumerate([2, 3, 1, 2], 1)]
    }

    reportes_mes = execute_query("""
        SELECT DATE_FORMAT(fecha_reporte, '%Y-%m') as mes, COUNT(*) as total
        FROM Reportes WHERE fecha_reporte >= DATE_SUB(NOW(), INTERVAL 6 MONTH)
        GROUP BY DATE_FORMAT(fecha_reporte, '%Y-%m') ORDER BY mes
    """, fetch_all=True)
    if reportes_mes:
        for item in reportes_mes:
            try:
                year, month = item['mes'].split('-')
                item['mes'] = calendar.month_name[int(month)][:3] + " " + year
            except Exception:
                pass
        stats['reportes_mes'] = reportes_mes

    severidad = execute_query("""
        SELECT gravedad, COUNT(*) as total FROM Reportes GROUP BY gravedad
        ORDER BY CASE gravedad WHEN 'critico' THEN 1 WHEN 'severo' THEN 2
            WHEN 'moderado' THEN 3 WHEN 'leve' THEN 4 END
    """, fetch_all=True)
    if severidad:
        stats['severidad'] = severidad

    evolucion = execute_query("""
        SELECT WEEK(fecha_reporte) as semana, COUNT(*) as total
        FROM Reportes WHERE fecha_reporte >= DATE_SUB(NOW(), INTERVAL 8 WEEK)
        GROUP BY WEEK(fecha_reporte) ORDER BY semana
    """, fetch_all=True)
    if evolucion:
        stats['evolucion'] = [{'semana': i + 1, 'total': item['total']}
                              for i, item in enumerate(evolucion)]

    return stats
