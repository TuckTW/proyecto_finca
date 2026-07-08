from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from django.contrib.auth.decorators import login_required

@login_required
def listar_alimentacion(request):
    alimentacion = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT g.codigo, g.nombre, a.tipo_alimento, a.cantidad, a.fecha
                FROM alimentacion a
                INNER JOIN ganado g ON a.id_ganado = g.id_ganado
                ORDER BY a.fecha DESC
                LIMIT 20
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
            
            # Obtener el ID del usuario actual
            with connection.cursor() as cursor:
                cursor.execute("SELECT id_usuario FROM usuarios WHERE usuario = %s", [request.user.username])
                result = cursor.fetchone()
                if not result:
                    messages.error(request, '❌ Usuario no encontrado en la base de datos')
                    return redirect('alimentacion:listar_alimentacion')
                usuario_id = result[0]
                
                cursor.callproc('sp_registrar_alimentacion', [
                    animal, usuario_id, tipo_alimento, cantidad, fecha
                ])
            messages.success(request, '✅ Alimentación registrada exitosamente')
            return redirect('alimentacion:listar_alimentacion')
        except Exception as e:
            messages.error(request, f'❌ Error: {str(e)}')
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
                    messages.error(request, '❌ Usuario no encontrado')
                    return redirect('alimentacion:listar_pesajes')
                usuario_id = result[0]
                
                cursor.callproc('sp_registrar_pesaje', [
                    animal, usuario_id, fecha, peso, observaciones
                ])
            messages.success(request, '✅ Pesaje registrado exitosamente')
            return redirect('alimentacion:listar_pesajes')
        except Exception as e:
            messages.error(request, f'❌ Error: {str(e)}')
            return redirect('alimentacion:listar_pesajes')
    
    animales = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_ganado, codigo, nombre FROM ganado")
            animales = cursor.fetchall()
    except Exception as e:
        messages.warning(request, f'Error: {e}')
    
    return render(request, 'alimentacion/registrar_pesaje.html', {'animales': animales})
