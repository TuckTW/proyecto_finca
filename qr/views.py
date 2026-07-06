from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import connection
from ganado.models import Ganado
import qrcode
import base64
from io import BytesIO

@login_required
def index(request):
    animales = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT g.id_ganado, g.codigo, g.nombre, r.nombre as raza, g.peso_actual
                FROM ganado g
                INNER JOIN razas r ON g.id_raza = r.id_raza
                ORDER BY g.id_ganado
            """)
            animales = cursor.fetchall()
    except Exception as e:
        print(f'Error: {e}')
    
    return render(request, 'qr/index.html', {'animales': animales})

@login_required
def generar_qr(request, id):
    animal = get_object_or_404(Ganado, pk=id)
    
    # Crear datos para el QR
    qr_data = f"""
    === FINCA EL PUENTE ===
    Código: {animal.codigo}
    Nombre: {animal.nombre}
    Raza: {animal.id_raza.nombre}
    Sexo: {animal.sexo}
    Peso: {animal.peso_actual} kg
    Estado: {animal.estado}
    """
    
    # Generar QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convertir a base64
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    context = {
        'animal': animal,
        'qr_image': image_base64,
        'qr_data': qr_data,
    }
    
    return render(request, 'qr/ver_qr.html', context)

def escanear_qr(request, codigo):
    try:
        animal = Ganado.objects.select_related('id_raza').get(codigo=codigo)
        
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT v.nombre, h.fecha, h.proxima_fecha
                FROM historial_vacunacion h
                INNER JOIN vacunas v ON h.id_vacuna = v.id_vacuna
                WHERE h.id_ganado = %s
                ORDER BY h.fecha DESC
                LIMIT 3
            """, [animal.id_ganado])
            vacunas = cursor.fetchall()
        
        context = {'animal': animal, 'vacunas': vacunas}
        return render(request, 'qr/datos_movil.html', context)
    except Ganado.DoesNotExist:
        return render(request, 'qr/error.html', {'mensaje': 'Animal no encontrado'})
