"""
Vistas API.
"""
from django.http import JsonResponse
from ..decorators import session_required
from ..services import get_chart_statistics

@session_required
def api_reportes(request):
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT R.id, R.ubicacion, R.barrio as zona, T.nombre_anomalia as tipo_anomalia,
                R.gravedad, R.descripcion, R.info_adicional, R.fecha_reporte, R.estado,
                R.latitud as lat, R.longitud as lng, R.imagen, R.imagen2, R.imagen3,
                U.nombre_usuario AS reportado_por
            FROM reportes R
            LEFT JOIN usuarios U ON R.usuario_id = U.id
            LEFT JOIN tiposanomalia T ON R.id_tipo_anomalia = T.id
            ORDER BY R.fecha_reporte DESC
        """)
        cols = [col[0] for col in cursor.description]
        reportes = [dict(zip(cols, row)) for row in cursor.fetchall()]

    for r in reportes:
        if r['fecha_reporte']:
            r['fecha_reporte'] = r['fecha_reporte'].strftime('%Y-%m-%d %H:%M:%S')
        r['image_url'] = f"/media/{r['imagen']}" if r['imagen'] else None
        r['image_url2'] = f"/media/{r['imagen2']}" if r['imagen2'] else None
        r['image_url3'] = f"/media/{r['imagen3']}" if r['imagen3'] else None

    return JsonResponse(reportes, safe=False)

@session_required
def api_estadisticas(request):
    return JsonResponse(get_chart_statistics())

def mapa_html(request):
    from django.shortcuts import render
    return render(request, "safezone_app/mapa.html")

def estadisticas_html(request):
    from django.shortcuts import render
    return render(request, "safezone_app/estadisticas.html")
