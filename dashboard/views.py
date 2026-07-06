from django.shortcuts import render
from django.db import connection
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    stats = {
        'total_ganado': 0,
        'ganado_activo': 0,
        'ganado_enfermo': 0,
        'peso_promedio': 0
    }
    
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
    except Exception as e:
        print(f"Error en dashboard: {e}")
    
    return render(request, 'dashboard/index.html', {'stats': stats})
