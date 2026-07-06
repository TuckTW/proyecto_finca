from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from django.contrib.auth.decorators import login_required

@login_required
def listar_ganado(request):
    ganado = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT g.*, r.nombre as raza_nombre 
                FROM ganado g 
                INNER JOIN razas r ON g.id_raza = r.id_raza
                ORDER BY g.id_ganado DESC
            """)
            ganado = cursor.fetchall()
    except Exception as e:
        messages.warning(request, f'Error al cargar datos: {e}')
    
    return render(request, 'ganado/listar.html', {'ganado': ganado})

@login_required
def registrar_ganado(request):
    if request.method == 'POST':
        try:
            codigo = request.POST.get('codigo')
            nombre = request.POST.get('nombre')
            raza = request.POST.get('raza')
            sexo = request.POST.get('sexo')
            fecha_nacimiento = request.POST.get('fecha_nacimiento') or None
            peso_inicial = request.POST.get('peso_inicial') or None
            estado = request.POST.get('estado')
            color = request.POST.get('color', '')
            observaciones = request.POST.get('observaciones', '')
            
            with connection.cursor() as cursor:
                cursor.callproc('sp_registrar_ganado', [
                    codigo, nombre, raza, sexo, fecha_nacimiento,
                    peso_inicial, estado, color, '', observaciones
                ])
            messages.success(request, f'✅ Animal {nombre} registrado exitosamente')
            return redirect('ganado:listar_ganado')
        except Exception as e:
            messages.error(request, f'❌ Error al registrar: {str(e)}')
            return redirect('ganado:listar_ganado')
    
    razas = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_raza, nombre FROM razas")
            razas = cursor.fetchall()
    except Exception as e:
        messages.warning(request, f'Error: {e}')
    
    return render(request, 'ganado/registrar.html', {'razas': razas})

@login_required
def editar_ganado(request, id):
    if request.method == 'POST':
        messages.success(request, f'✅ Animal {id} actualizado (demo)')
        return redirect('ganado:listar_ganado')
    return render(request, 'ganado/editar.html', {'id': id})

@login_required
def eliminar_ganado(request, id):
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_eliminar_ganado', [id])
            messages.success(request, f'✅ Animal {id} eliminado')
        except Exception as e:
            messages.error(request, f'❌ Error: {str(e)}')
    return redirect('ganado:listar_ganado')

@login_required
def buscar_ganado(request):
    return render(request, 'ganado/buscar.html')
