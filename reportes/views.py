from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
import io
import pandas as pd
from datetime import datetime
from django.db.models import Count, Avg
from ganado.models import Ganado

@login_required
def index(request):
    return render(request, 'reportes/index.html')

@login_required
def reporte_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_ganado.pdf"'

    doc = SimpleDocTemplate(response, pagesize=landscape(A4))
    elementos = []
    styles = getSampleStyleSheet()

    titulo = Paragraph("Finca El Puente - Reporte de Ganado", styles['Title'])
    elementos.append(titulo)
    elementos.append(Spacer(1, 20))

    fecha = Paragraph(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal'])
    elementos.append(fecha)
    elementos.append(Spacer(1, 20))

    ganado_list = Ganado.objects.select_related('id_raza').order_by('id_ganado')

    if ganado_list.exists():
        data = [['Codigo', 'Nombre', 'Raza', 'Sexo', 'Peso (kg)', 'Estado', 'Registro']]
        for g in ganado_list:
            data.append([
                g.codigo,
                g.nombre,
                g.id_raza.nombre if g.id_raza else '-',
                g.sexo,
                str(g.peso_actual or '0'),
                g.estado,
                g.fecha_registro.strftime('%d/%m/%Y') if g.fecha_registro else '-'
            ])

        table = Table(data, colWidths=[2*cm, 3*cm, 2.5*cm, 2*cm, 2*cm, 2.5*cm, 3*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
        ]))
        elementos.append(table)
    else:
        elementos.append(Paragraph("No hay datos disponibles", styles['Normal']))

    doc.build(elementos)
    return response

@login_required
def reporte_excel(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="reporte_ganado.xlsx"'

    ganado_list = Ganado.objects.select_related('id_raza').order_by('id_ganado')
    datos = []

    for g in ganado_list:
        fecha_limpia = g.fecha_registro.replace(tzinfo=None) if g.fecha_registro else None
        datos.append([
            g.codigo,
            g.nombre,
            g.id_raza.nombre if g.id_raza else '-',
            g.sexo,
            g.peso_actual,
            g.estado,
            fecha_limpia
        ])

    if datos:
        df = pd.DataFrame(datos, columns=['Codigo', 'Nombre', 'Raza', 'Sexo', 'Peso (kg)', 'Estado', 'Fecha Registro'])
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Ganado', index=False)
    else:
        response.write(b'No hay datos disponibles')

    return response

@login_required
def estadisticas(request):
    estados_qs = Ganado.objects.values('estado').annotate(total=Count('estado'))
    por_estado = [(item['estado'], item['total']) for item in estados_qs]

    razas_qs = Ganado.objects.values('id_raza__nombre').annotate(total=Count('id_raza'))
    por_raza = [(item['id_raza__nombre'], item['total']) for item in razas_qs]

    peso_prom_dict = Ganado.objects.aggregate(Avg('peso_actual'))
    peso_prom = peso_prom_dict['peso_actual__avg'] or 0

    total = Ganado.objects.count()

    from django.db import connection
    with connection.cursor() as cursor:
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
            SELECT g.codigo, g.nombre, r.nombre,
                   g.peso_inicial, g.peso_actual,
                   (g.peso_actual - g.peso_inicial) AS ganancia
            FROM ganado g
            JOIN razas r ON g.id_raza = r.id_raza
            WHERE g.peso_inicial IS NOT NULL AND g.peso_actual IS NOT NULL
            ORDER BY ganancia DESC
        """)
        ganancias_peso = cursor.fetchall()

    context = {
        'por_estado': por_estado,
        'por_raza': por_raza,
        'peso_promedio': round(float(peso_prom), 2),
        'total': total,
        'vacunas_proximas': vacunas_proximas,
        'ganancias_peso': ganancias_peso,
    }

    return render(request, 'reportes/estadisticas.html', context)
