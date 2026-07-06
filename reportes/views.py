from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import connection
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
import io
import pandas as pd
from datetime import datetime

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
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT g.codigo, g.nombre, r.nombre as raza, g.sexo, 
                   g.peso_actual, g.estado, g.fecha_registro
            FROM ganado g
            INNER JOIN razas r ON g.id_raza = r.id_raza
            ORDER BY g.id_ganado
        """)
        datos = cursor.fetchall()
    
    if datos:
        data = [['Código', 'Nombre', 'Raza', 'Sexo', 'Peso (kg)', 'Estado', 'Registro']]
        for d in datos:
            data.append([
                d[0], d[1], d[2], d[3], 
                str(d[4] or '0'), d[5], 
                d[6].strftime('%d/%m/%Y') if d[6] else '-'
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
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT g.codigo, g.nombre, r.nombre as raza, g.sexo, 
                   g.peso_actual, g.estado, g.fecha_registro
            FROM ganado g
            INNER JOIN razas r ON g.id_raza = r.id_raza
            ORDER BY g.id_ganado
        """)
        datos = cursor.fetchall()
    
    if datos:
        df = pd.DataFrame(datos, columns=['Código', 'Nombre', 'Raza', 'Sexo', 'Peso (kg)', 'Estado', 'Fecha Registro'])
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Ganado', index=False)
    else:
        response.write(b'No hay datos disponibles')
    
    return response

@login_required
def estadisticas(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT estado, COUNT(*) as total FROM ganado GROUP BY estado")
        por_estado = cursor.fetchall()
        
        cursor.execute("""
            SELECT r.nombre, COUNT(*) as total
            FROM ganado g
            INNER JOIN razas r ON g.id_raza = r.id_raza
            GROUP BY r.nombre
        """)
        por_raza = cursor.fetchall()
        
        cursor.execute("SELECT AVG(peso_actual) FROM ganado")
        peso_prom = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT COUNT(*) FROM ganado")
        total = cursor.fetchone()[0]
    
    context = {
        'por_estado': por_estado,
        'por_raza': por_raza,
        'peso_promedio': round(float(peso_prom), 2),
        'total': total,
    }
    
    return render(request, 'reportes/estadisticas.html', context)
