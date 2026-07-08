from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from ganado.models import Ganado
from .models import Notificacion

@login_required
def dashboard(request):
    stats = {
        'total_ganado': 0,
        'ganado_activo': 0,
        'ganado_enfermo': 0,
        'peso_promedio': 0
    }
    vacunas_proximas = []
    distribucion_estado = []
    distribucion_raza = []
    aumento_peso = []
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM ganado")
            result = cursor.fetchone()
            stats['total_ganado'] = result[0] if result else 0
            
            cursor.execute("SELECT COUNT(*) FROM ganado WHERE estado = 'Activo'")
            result = cursor.fetchone()
            stats['ganado_activo'] = result[0] if result else 0
            
            cursor.execute("SELECT COUNT(*) FROM ganado WHERE estado = 'Enfermo'")
            result = cursor.fetchone()
            stats['ganado_enfermo'] = result[0] if result else 0
            
            cursor.execute("SELECT AVG(peso_actual) FROM ganado")
            result = cursor.fetchone()
            stats['peso_promedio'] = float(result[0]) if result and result[0] else 0

            cursor.execute("""
                SELECT g.codigo, g.nombre, v.nombre, h.proxima_fecha
                FROM historial_vacunacion h
                JOIN ganado g ON h.id_ganado = g.id_ganado
                JOIN vacunas v ON h.id_vacuna = v.id_vacuna
                WHERE h.proxima_fecha <= CURDATE() + INTERVAL 30 DAY
                  AND h.proxima_fecha >= CURDATE()
                ORDER BY h.proxima_fecha ASC
            """)
            vacunas_proximas = cursor.fetchall()

            cursor.execute("""
                SELECT estado, COUNT(*)
                FROM ganado
                WHERE estado IS NOT NULL AND estado != 'Muerto'
                GROUP BY estado
                ORDER BY COUNT(*) DESC
            """)
            distribucion_estado = cursor.fetchall()

            cursor.execute("""
                SELECT r.nombre, COUNT(g.id_ganado)
                FROM razas r
                LEFT JOIN ganado g ON r.id_raza = g.id_raza
                GROUP BY r.id_raza, r.nombre
                ORDER BY COUNT(g.id_ganado) DESC
            """)
            distribucion_raza = cursor.fetchall()

            cursor.execute("""
                SELECT DATE_FORMAT(fecha, '%Y-%m') as mes, AVG(peso)
                FROM pesajes
                GROUP BY DATE_FORMAT(fecha, '%Y-%m')
                ORDER BY mes ASC
            """)
            aumento_peso = cursor.fetchall()
    except Exception as e:
        print(f"Error en dashboard: {e}")
    
    colores_estado = {'Activo': '#2ecc71', 'Enfermo': '#e74c3c', 'Recuperacion': '#f1c40f'}
    colores_raza = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c', '#e67e22', '#34495e', '#e91e63', '#00bcd4']

    chart_estado = {
        'labels': [e[0] for e in distribucion_estado],
        'data': [e[1] for e in distribucion_estado],
        'colors': [colores_estado.get(e[0], '#95a5a6') for e in distribucion_estado],
    }
    chart_raza = {
        'labels': [r[0] for r in distribucion_raza],
        'data': [r[1] for r in distribucion_raza],
        'colors': colores_raza[:len(distribucion_raza)],
    }
    chart_peso = {
        'labels': [m[0] for m in aumento_peso],
        'data': [float(m[1]) if m[1] is not None else 0 for m in aumento_peso],
    }

    return render(request, 'dashboard/index.html', {
        'stats': stats,
        'vacunas_proximas': vacunas_proximas,
        'chart_estado': chart_estado,
        'chart_raza': chart_raza,
        'chart_peso': chart_peso,
    })

@login_required
def marcar_notificaciones_leidas(request):
    Notificacion.objects.filter(usuario=request.user, leido=False).update(leido=True)
    return redirect(request.META.get('HTTP_REFERER', '/'))
