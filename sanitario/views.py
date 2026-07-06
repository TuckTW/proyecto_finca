from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from django.contrib.auth.decorators import login_required

@login_required
def listar_vacunas(request):
    vacunaciones = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT g.codigo, g.nombre, v.nombre as vacuna, 
                       h.fecha, h.proxima_fecha
                FROM historial_vacunacion h
                INNER JOIN ganado g ON h.id_ganado = g.id_ganado
                INNER JOIN vacunas v ON h.id_vacuna = v.id_vacuna
                ORDER BY h.fecha DESC
                LIMIT 20
            """)
            vacunaciones = cursor.fetchall()
    except Exception as e:
        messages.warning(request, f'Error: {e}')
    
    return render(request, 'sanitario/listar.html', {'vacunaciones': vacunaciones})

@login_required
def registrar_vacunacion(request):
    if request.method == 'POST':
        try:
            animal = request.POST.get('animal')
            vacuna = request.POST.get('vacuna')
            fecha = request.POST.get('fecha')
            proxima_fecha = request.POST.get('proxima_fecha') or None
            observaciones = request.POST.get('observaciones', '')
            
            # Obtener el ID del usuario actual desde la tabla usuarios
            with connection.cursor() as cursor:
                cursor.execute("SELECT id_usuario FROM usuarios WHERE usuario = %s", [request.user.username])
                result = cursor.fetchone()
                if not result:
                    messages.error(request, '❌ Usuario no encontrado en la base de datos')
                    return redirect('sanitario:listar_vacunas')
                usuario_id = result[0]
                
                cursor.callproc('sp_registrar_vacunacion', [
                    animal, vacuna, usuario_id, fecha, proxima_fecha, observaciones
                ])
            messages.success(request, '✅ Vacunación registrada exitosamente')
            return redirect('sanitario:listar_vacunas')
        except Exception as e:
            messages.error(request, f'❌ Error: {str(e)}')
            return redirect('sanitario:listar_vacunas')
    
    # Obtener lista de animales y vacunas para el formulario
    animales = []
    vacunas = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_ganado, codigo, nombre FROM ganado WHERE estado='Activo'")
            animales = cursor.fetchall()
            cursor.execute("SELECT id_vacuna, nombre FROM vacunas")
            vacunas = cursor.fetchall()
    except Exception as e:
        messages.warning(request, f'Error al cargar datos: {e}')
    
    return render(request, 'sanitario/registrar.html', {
        'animales': animales,
        'vacunas': vacunas
    })

@login_required
def listar_tratamientos(request):
    tratamientos = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT g.codigo, g.nombre, e.nombre as enfermedad, 
                       t.medicamento, t.fecha_inicio, t.fecha_fin
                FROM tratamientos t
                INNER JOIN ganado g ON t.id_ganado = g.id_ganado
                INNER JOIN enfermedades e ON t.id_enfermedad = e.id_enfermedad
                ORDER BY t.fecha_inicio DESC
                LIMIT 20
            """)
            tratamientos = cursor.fetchall()
    except Exception as e:
        messages.warning(request, f'Error: {e}')
    
    return render(request, 'sanitario/tratamientos.html', {'tratamientos': tratamientos})

@login_required
def registrar_tratamiento(request):
    if request.method == 'POST':
        try:
            animal = request.POST.get('animal')
            enfermedad = request.POST.get('enfermedad')
            medicamento = request.POST.get('medicamento')
            fecha_inicio = request.POST.get('fecha_inicio')
            fecha_fin = request.POST.get('fecha_fin') or None
            observaciones = request.POST.get('observaciones', '')
            
            with connection.cursor() as cursor:
                cursor.execute("SELECT id_usuario FROM usuarios WHERE usuario = %s", [request.user.username])
                result = cursor.fetchone()
                if not result:
                    messages.error(request, '❌ Usuario no encontrado')
                    return redirect('sanitario:listar_tratamientos')
                usuario_id = result[0]
                
                cursor.callproc('sp_registrar_tratamiento', [
                    animal, enfermedad, usuario_id, medicamento, 
                    fecha_inicio, fecha_fin, observaciones
                ])
            messages.success(request, '✅ Tratamiento registrado exitosamente')
            return redirect('sanitario:listar_tratamientos')
        except Exception as e:
            messages.error(request, f'❌ Error: {str(e)}')
            return redirect('sanitario:listar_tratamientos')
    
    animales = []
    enfermedades = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_ganado, codigo, nombre FROM ganado")
            animales = cursor.fetchall()
            cursor.execute("SELECT id_enfermedad, nombre FROM enfermedades")
            enfermedades = cursor.fetchall()
    except Exception as e:
        messages.warning(request, f'Error: {e}')
    
    return render(request, 'sanitario/registrar_tratamiento.html', {
        'animales': animales,
        'enfermedades': enfermedades
    })
