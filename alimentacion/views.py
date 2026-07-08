from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from django.contrib.auth.decorators import login_required
from dashboard.models import Notificacion

@login_required
def listar_alimentacion(request):
    alimentacion = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT a.id_alimentacion, g.codigo, g.nombre, a.tipo_alimento, a.cantidad, a.fecha
                FROM alimentacion a
                INNER JOIN ganado g ON a.id_ganado = g.id_ganado
                ORDER BY a.fecha DESC
                LIMIT 50
            """)
            alimentacion = cursor.fetchall()
    except Exception as e:
        messages.warning(request, f'Error: {e}')
    return render(request, 'alimentacion/listar.html', {'alimentacion': alimentacion})

@login_required
def registrar_alimentacion(request):
    if request.method == 'POST':
        try:
            animal = request.POST.get('animal')
            tipo_alimento = request.POST.get('tipo_alimento')
            cantidad = request.POST.get('cantidad')
            fecha = request.POST.get('fecha')

            with connection.cursor() as cursor:
                cursor.execute("SELECT id_usuario FROM usuarios WHERE usuario = %s", [request.user.username])
                result = cursor.fetchone()
                if not result:
                    messages.error(request, 'Usuario no encontrado en la base de datos')
                    return redirect('alimentacion:listar_alimentacion')
                usuario_id = result[0]
                cursor.callproc('sp_registrar_alimentacion', [
                    animal, usuario_id, tipo_alimento, cantidad, fecha
                ])

            with connection.cursor() as cursor:
                cursor.execute("SELECT codigo, nombre FROM ganado WHERE id_ganado = %s", [animal])
                anim = cursor.fetchone()
                anim_text = f"{anim[0]} - {anim[1]}" if anim else animal

            Notificacion.objects.create(
                usuario=request.user,
                titulo="Alimento Registrado",
                mensaje=f"Se registro alimentacion ({tipo_alimento}, {cantidad} kg) para {anim_text}.",
                tipo="Exito"
            )
            messages.success(request, 'Alimentacion registrada exitosamente')
            return redirect('alimentacion:listar_alimentacion')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('alimentacion:listar_alimentacion')

    animales = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_ganado, codigo, nombre FROM ganado ORDER BY codigo")
            animales = cursor.fetchall()
    except Exception as e:
        messages.warning(request, f'Error: {e}')
    return render(request, 'alimentacion/registrar.html', {'animales': animales})

@login_required
def editar_alimentacion(request, id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT a.id_alimentacion, a.id_ganado, a.tipo_alimento, a.cantidad, a.fecha
            FROM alimentacion a WHERE a.id_alimentacion = %s
        """, [id])
        row = cursor.fetchone()
        if not row:
            messages.error(request, 'Registro no encontrado')
            return redirect('alimentacion:listar_alimentacion')

    if request.method == 'POST':
        try:
            animal = request.POST.get('animal')
            tipo_alimento = request.POST.get('tipo_alimento')
            cantidad = request.POST.get('cantidad')
            fecha = request.POST.get('fecha')

            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE alimentacion
                    SET id_ganado = %s, tipo_alimento = %s, cantidad = %s, fecha = %s
                    WHERE id_alimentacion = %s
                """, [animal, tipo_alimento, cantidad, fecha, id])

            Notificacion.objects.create(
                usuario=request.user,
                titulo="Alimento Actualizado",
                mensaje=f"El registro de alimentacion #{id} fue actualizado.",
                tipo="Exito"
            )
            messages.success(request, 'Alimentacion actualizada exitosamente')
            return redirect('alimentacion:listar_alimentacion')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('alimentacion:editar_alimentacion', id=id)

    animales = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_ganado, codigo, nombre FROM ganado ORDER BY codigo")
            animales = cursor.fetchall()
    except Exception as e:
        messages.warning(request, f'Error: {e}')
    return render(request, 'alimentacion/editar_alimento.html', {
        'ali': {'id_alimentacion': row[0], 'id_ganado': row[1],
                'tipo_alimento': row[2], 'cantidad': row[3], 'fecha': row[4]},
        'animales': animales,
    })

@login_required
def eliminar_alimentacion(request, id):
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM alimentacion WHERE id_alimentacion = %s", [id])
            Notificacion.objects.create(
                usuario=request.user,
                titulo="Alimento Eliminado",
                mensaje=f"El registro de alimentacion #{id} fue eliminado.",
                tipo="Alerta"
            )
            messages.success(request, 'Alimentacion eliminada')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    return redirect('alimentacion:listar_alimentacion')

@login_required
def listar_pesajes(request):
    pesajes = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT g.codigo, g.nombre, p.fecha, p.peso, p.observaciones
                FROM pesajes p
                INNER JOIN ganado g ON p.id_ganado = g.id_ganado
                ORDER BY p.fecha DESC
                LIMIT 20
            """)
            pesajes = cursor.fetchall()
    except Exception as e:
        messages.warning(request, f'Error: {e}')
    return render(request, 'alimentacion/pesajes.html', {'pesajes': pesajes})

@login_required
def registrar_pesaje(request):
    if request.method == 'POST':
        try:
            animal = request.POST.get('animal')
            fecha = request.POST.get('fecha')
            peso = request.POST.get('peso')
            observaciones = request.POST.get('observaciones', '')

            with connection.cursor() as cursor:
                cursor.execute("SELECT id_usuario FROM usuarios WHERE usuario = %s", [request.user.username])
                result = cursor.fetchone()
                if not result:
                    messages.error(request, 'Usuario no encontrado')
                    return redirect('alimentacion:listar_pesajes')
                usuario_id = result[0]
                cursor.callproc('sp_registrar_pesaje', [
                    animal, usuario_id, fecha, peso, observaciones
                ])
            messages.success(request, 'Pesaje registrado exitosamente')
            return redirect('alimentacion:listar_pesajes')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('alimentacion:listar_pesajes')

    animales = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_ganado, codigo, nombre FROM ganado")
            animales = cursor.fetchall()
    except Exception as e:
        messages.warning(request, f'Error: {e}')
    return render(request, 'alimentacion/registrar_pesaje.html', {'animales': animales})
