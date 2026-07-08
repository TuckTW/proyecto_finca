from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import connection
from .models import Ganado, Raza
from dashboard.models import Notificacion
from sanitario.services import calcular_recomendaciones_vacunas

@login_required
def listar_ganado(request):
    try:
        ganado = Ganado.objects.select_related('id_raza').all().order_by('-id_ganado')
    except Exception as e:
        ganado = []
        messages.warning(request, f'Error al cargar datos: {e}')
    return render(request, 'ganado/listar.html', {'ganado': ganado})

@login_required
def registrar_ganado(request):
    if request.method == 'POST':
        try:
            codigo = request.POST.get('codigo')
            nombre = request.POST.get('nombre')
            raza_id = request.POST.get('raza')
            sexo = request.POST.get('sexo')
            fecha_nacimiento = request.POST.get('fecha_nacimiento') or None
            peso_inicial = request.POST.get('peso_inicial') or None
            estado = request.POST.get('estado')
            color = request.POST.get('color', '')
            observaciones = request.POST.get('observaciones', '')
            vacuna_id = request.POST.get('vacuna') or None
            fecha_vac = request.POST.get('fecha_vacunacion') or None
            proxima_vac = request.POST.get('proxima_vacunacion') or None

            raza = get_object_or_404(Raza, pk=raza_id)

            animal = Ganado.objects.create(
                codigo=codigo,
                nombre=nombre,
                id_raza=raza,
                sexo=sexo,
                fecha_nacimiento=fecha_nacimiento,
                peso_inicial=peso_inicial,
                peso_actual=peso_inicial,
                estado=estado,
                color=color,
                observaciones=observaciones
            )

            if vacuna_id and fecha_vac:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT id_usuario FROM usuarios WHERE usuario = %s", [request.user.username])
                    result = cursor.fetchone()
                    usuario_id = result[0] if result else 1
                    cursor.callproc('sp_registrar_vacunacion', [
                        animal.id_ganado, vacuna_id, usuario_id,
                        fecha_vac, proxima_vac, 'Vacuna inicial al registrar'
                    ])

            Notificacion.objects.create(
                usuario=request.user,
                titulo="Nuevo Ingreso",
                mensaje=f"El animal {nombre} ({codigo}) fue registrado exitosamente en el sistema.",
                tipo="Exito"
            )

            messages.success(request, f'Animal {nombre} registrado exitosamente')
            return redirect('ganado:listar_ganado')
        except Exception as e:
            messages.error(request, f'Error al registrar: {str(e)}')
            return redirect('ganado:listar_ganado')

    try:
        razas = Raza.objects.all()
        vacunas = []
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_vacuna, nombre FROM vacunas")
            vacunas = cursor.fetchall()
    except Exception as e:
        razas = []
        vacunas = []
        messages.warning(request, f'Error: {e}')

    return render(request, 'ganado/registrar.html', {'razas': razas, 'vacunas': vacunas})

@login_required
def editar_ganado(request, id):
    animal = get_object_or_404(Ganado, pk=id)

    if request.method == 'POST':
        messages.success(request, f'Animal {id} actualizado (demo)')
        return redirect('ganado:listar_ganado')

    vacunas_sugeridas = calcular_recomendaciones_vacunas(animal)

    return render(request, 'ganado/editar.html', {
        'animal': animal,
        'id': id,
        'vacunas_sugeridas': vacunas_sugeridas
    })

@login_required
def eliminar_ganado(request, id):
    if request.method == 'POST':
        try:
            animal = get_object_or_404(Ganado, pk=id)
            animal.delete()
            messages.success(request, f'Animal {id} eliminado')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    return redirect('ganado:listar_ganado')

@login_required
def buscar_ganado(request):
    return render(request, 'ganado/buscar.html')
