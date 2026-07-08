from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import connection
from django.contrib.auth.decorators import login_required
from dashboard.models import Notificacion

@login_required
def listar_vacunas(request):
    vacunaciones = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT h.id_historial, g.codigo, g.nombre, v.nombre as vacuna, 
                       h.fecha, h.proxima_fecha, h.observaciones
                FROM historial_vacunacion h
                INNER JOIN ganado g ON h.id_ganado = g.id_ganado
                INNER JOIN vacunas v ON h.id_vacuna = v.id_vacuna
                ORDER BY h.fecha DESC
                LIMIT 50
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

            with connection.cursor() as cursor:
                cursor.execute("SELECT id_usuario FROM usuarios WHERE usuario = %s", [request.user.username])
                result = cursor.fetchone()
                if not result:
                    messages.error(request, 'Usuario no encontrado en la base de datos')
                    return redirect('sanitario:listar_vacunas')
                usuario_id = result[0]
                cursor.callproc('sp_registrar_vacunacion', [
                    animal, vacuna, usuario_id, fecha, proxima_fecha, observaciones
                ])

            with connection.cursor() as cursor:
                cursor.execute("SELECT codigo, nombre FROM ganado WHERE id_ganado = %s", [animal])
                anim = cursor.fetchone()
                cursor.execute("SELECT nombre FROM vacunas WHERE id_vacuna = %s", [vacuna])
                vac = cursor.fetchone()
                anim_text = f"{anim[0]} - {anim[1]}" if anim else animal
                vac_text = vac[0] if vac else vacuna

            Notificacion.objects.create(
                usuario=request.user,
                titulo="Vacuna Registrada",
                mensaje=f"Se registro vacunacion de {vac_text} para {anim_text}.",
                tipo="Exito"
            )
            messages.success(request, 'Vacunacion registrada exitosamente')
            return redirect('sanitario:listar_vacunas')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('sanitario:listar_vacunas')

    animales = []
    vacunas = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_ganado, codigo, nombre FROM ganado ORDER BY codigo")
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
def editar_vacunacion(request, id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT h.id_historial, h.id_ganado, h.id_vacuna, h.fecha, h.proxima_fecha, h.observaciones
            FROM historial_vacunacion h WHERE h.id_historial = %s
        """, [id])
        row = cursor.fetchone()
        if not row:
            messages.error(request, 'Registro no encontrado')
            return redirect('sanitario:listar_vacunas')

    if request.method == 'POST':
        try:
            animal = request.POST.get('animal')
            vacuna = request.POST.get('vacuna')
            fecha = request.POST.get('fecha')
            proxima_fecha = request.POST.get('proxima_fecha') or None
            observaciones = request.POST.get('observaciones', '')

            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE historial_vacunacion
                    SET id_ganado = %s, id_vacuna = %s, fecha = %s,
                        proxima_fecha = %s, observaciones = %s
                    WHERE id_historial = %s
                """, [animal, vacuna, fecha, proxima_fecha, observaciones, id])

            Notificacion.objects.create(
                usuario=request.user,
                titulo="Vacuna Actualizada",
                mensaje=f"El registro de vacunacion #{id} fue actualizado.",
                tipo="Exito"
            )
            messages.success(request, 'Vacunacion actualizada exitosamente')
            return redirect('sanitario:listar_vacunas')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('sanitario:editar_vacunacion', id=id)

    animales = []
    vacunas = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_ganado, codigo, nombre FROM ganado ORDER BY codigo")
            animales = cursor.fetchall()
            cursor.execute("SELECT id_vacuna, nombre FROM vacunas")
            vacunas = cursor.fetchall()
    except Exception as e:
        messages.warning(request, f'Error: {e}')
    return render(request, 'sanitario/editar_vacuna.html', {
        'vac': {'id_historial': row[0], 'id_ganado': row[1], 'id_vacuna': row[2],
                'fecha': row[3], 'proxima_fecha': row[4], 'observaciones': row[5]},
        'animales': animales,
        'vacunas': vacunas,
    })

@login_required
def eliminar_vacunacion(request, id):
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM historial_vacunacion WHERE id_historial = %s", [id])
            Notificacion.objects.create(
                usuario=request.user,
                titulo="Vacuna Eliminada",
                mensaje=f"El registro de vacunacion #{id} fue eliminado.",
                tipo="Alerta"
            )
            messages.success(request, 'Vacunacion eliminada')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    return redirect('sanitario:listar_vacunas')

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
                    messages.error(request, 'Usuario no encontrado')
                    return redirect('sanitario:listar_tratamientos')
                usuario_id = result[0]
                cursor.callproc('sp_registrar_tratamiento', [
                    animal, enfermedad, usuario_id, medicamento,
                    fecha_inicio, fecha_fin, observaciones
                ])
            messages.success(request, 'Tratamiento registrado exitosamente')
            return redirect('sanitario:listar_tratamientos')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
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
