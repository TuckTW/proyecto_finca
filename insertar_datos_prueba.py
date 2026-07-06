#!/usr/bin/env python
import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finca_el_puente.settings')
django.setup()

from django.db import connection
from django.contrib.auth.models import User

def insertar_datos():
    print("=== INSERTANDO DATOS DE PRUEBA ===\n")
    
    with connection.cursor() as cursor:
        
        # 1. Insertar razas si no existen
        print("1. Insertando razas...")
        razas = ['Brahman', 'Hereford', 'Angus', 'Santa Gertrudis', 'Charolais']
        for raza in razas:
            cursor.execute("INSERT IGNORE INTO razas (nombre) VALUES (%s)", [raza])
        print(f"   ✅ {len(razas)} razas insertadas")
        
        # 2. Insertar vacunas
        print("\n2. Insertando vacunas...")
        vacunas = [
            ('Fiebre Aftosa', 'Vacuna contra fiebre aftosa', '5ml'),
            ('Brucelosis', 'Vacuna contra brucelosis', '2ml'),
            ('Carbunclo', 'Vacuna contra carbunclo sintomático', '3ml'),
            ('Rabia', 'Vacuna contra rabia', '2ml'),
            ('Pasteurelosis', 'Vacuna contra pasteurelosis', '4ml')
        ]
        for vacuna in vacunas:
            cursor.execute(
                "INSERT IGNORE INTO vacunas (nombre, descripcion, dosis) VALUES (%s, %s, %s)",
                [vacuna[0], vacuna[1], vacuna[2]]
            )
        print(f"   ✅ {len(vacunas)} vacunas insertadas")
        
        # 3. Insertar enfermedades
        print("\n3. Insertando enfermedades...")
        enfermedades = [
            ('Fiebre', 'Fiebre alta, pérdida de apetito'),
            ('Diarrea', 'Diarrea severa, deshidratación'),
            ('Neumonía', 'Tos, dificultad respiratoria'),
            ('Parásitos', 'Parásitos internos y externos'),
            ('Coquera', 'Cojeera, inflamación en patas')
        ]
        for enfermedad in enfermedades:
            cursor.execute(
                "INSERT IGNORE INTO enfermedades (nombre, descripcion) VALUES (%s, %s)",
                [enfermedad[0], enfermedad[1]]
            )
        print(f"   ✅ {len(enfermedades)} enfermedades insertadas")
        
        # 4. Insertar ganado (5 animales)
        print("\n4. Insertando ganado...")
        # Obtener IDs de razas
        cursor.execute("SELECT id_raza, nombre FROM razas")
        razas_dict = {row[1]: row[0] for row in cursor.fetchall()}
        
        animales = [
            ('BHM001', 'Luna', 'Brahman', 'Hembra', date(2024, 1, 15), 120, 'Activo', 'Blanco'),
            ('BHM002', 'Toro', 'Brahman', 'Macho', date(2023, 8, 20), 380, 'Activo', 'Gris'),
            ('BHM003', 'Estrella', 'Hereford', 'Hembra', date(2024, 3, 10), 95, 'Activo', 'Rojo'),
            ('BHM004', 'Negro', 'Angus', 'Macho', date(2023, 11, 5), 310, 'Activo', 'Negro'),
            ('BHM005', 'Blanca', 'Santa Gertrudis', 'Hembra', date(2024, 5, 1), 85, 'Activo', 'Blanco'),
        ]
        
        for animal in animales:
            id_raza = razas_dict.get(animal[2])
            if id_raza:
                cursor.callproc('sp_registrar_ganado', [
                    animal[0],  # codigo
                    animal[1],  # nombre
                    id_raza,    # id_raza
                    animal[3],  # sexo
                    animal[4],  # fecha_nacimiento
                    animal[5],  # peso_inicial
                    animal[6],  # estado
                    animal[7],  # color
                    '',         # foto
                    f'Animal registrado en prueba'  # observaciones
                ])
        print(f"   ✅ {len(animales)} animales insertados")
        
        # 5. Insertar vacunaciones
        print("\n5. Insertando vacunaciones...")
        # Obtener IDs
        cursor.execute("SELECT id_ganado, codigo FROM ganado")
        ganado_dict = {row[1]: row[0] for row in cursor.fetchall()}
        
        cursor.execute("SELECT id_vacuna, nombre FROM vacunas")
        vacunas_dict = {row[1]: row[0] for row in cursor.fetchall()}
        
        # Obtener un usuario (el superusuario)
        cursor.execute("SELECT id_usuario FROM usuarios LIMIT 1")
        usuario_id = cursor.fetchone()
        if not usuario_id:
            print("   ⚠️ No hay usuarios, creando superusuario...")
            # El superusuario ya debería existir
            cursor.execute("INSERT IGNORE INTO usuarios (nombre, usuario, clave, id_rol) VALUES ('Admin', 'admin', 'admin123', 1)")
            cursor.execute("SELECT id_usuario FROM usuarios LIMIT 1")
            usuario_id = cursor.fetchone()
        
        if usuario_id:
            usuario_id = usuario_id[0]
            
            vacunaciones = [
                ('BHM001', 'Fiebre Aftosa', date(2025, 6, 1), date(2026, 6, 1)),
                ('BHM001', 'Brucelosis', date(2025, 7, 15), date(2026, 7, 15)),
                ('BHM002', 'Fiebre Aftosa', date(2025, 5, 20), date(2026, 5, 20)),
                ('BHM002', 'Rabia', date(2025, 8, 10), date(2026, 8, 10)),
                ('BHM003', 'Carbunclo', date(2025, 6, 30), date(2026, 6, 30)),
            ]
            
            for vac in vacunaciones:
                id_ganado = ganado_dict.get(vac[0])
                id_vacuna = vacunas_dict.get(vac[1])
                if id_ganado and id_vacuna:
                    cursor.callproc('sp_registrar_vacunacion', [
                        id_ganado,
                        id_vacuna,
                        usuario_id,
                        vac[2],  # fecha
                        vac[3],  # proxima_fecha
                        'Vacunación de rutina'
                    ])
            print(f"   ✅ {len(vacunaciones)} vacunaciones insertadas")
        
        # 6. Insertar pesajes
        print("\n6. Insertando pesajes...")
        if usuario_id:
            pesajes = [
                ('BHM001', date(2025, 7, 1), 145, 'Peso normal'),
                ('BHM001', date(2025, 8, 1), 160, 'Buena ganancia'),
                ('BHM002', date(2025, 7, 1), 400, 'Peso excelente'),
                ('BHM003', date(2025, 7, 15), 110, 'Crecimiento adecuado'),
                ('BHM004', date(2025, 6, 30), 330, 'Peso bueno'),
            ]
            
            for pesaje in pesajes:
                id_ganado = ganado_dict.get(pesaje[0])
                if id_ganado:
                    cursor.callproc('sp_registrar_pesaje', [
                        id_ganado,
                        usuario_id,
                        pesaje[1],  # fecha
                        pesaje[2],  # peso
                        pesaje[3]   # observaciones
                    ])
            print(f"   ✅ {len(pesajes)} pesajes insertados")
        
        # 7. Insertar alimentación
        print("\n7. Insertando alimentación...")
        if usuario_id:
            alimentos = [
                ('BHM001', 'Pasto', 25.5, date(2025, 7, 1)),
                ('BHM001', 'Concentrado', 5.0, date(2025, 7, 2)),
                ('BHM002', 'Pasto', 40.0, date(2025, 7, 1)),
                ('BHM002', 'Concentrado', 8.0, date(2025, 7, 2)),
                ('BHM003', 'Pasto', 20.0, date(2025, 7, 1)),
            ]
            
            for alimento in alimentos:
                id_ganado = ganado_dict.get(alimento[0])
                if id_ganado:
                    cursor.callproc('sp_registrar_alimentacion', [
                        id_ganado,
                        usuario_id,
                        alimento[1],  # tipo_alimento
                        alimento[2],  # cantidad
                        alimento[3]   # fecha
                    ])
            print(f"   ✅ {len(alimentos)} registros de alimentación insertados")
        
        print("\n✅ ¡DATOS DE PRUEBA INSERTADOS CORRECTAMENTE!")
        print("\nResumen:")
        cursor.execute("SELECT COUNT(*) FROM ganado")
        print(f"  - Animales: {cursor.fetchone()[0]}")
        cursor.execute("SELECT COUNT(*) FROM vacunas")
        print(f"  - Vacunas: {cursor.fetchone()[0]}")
        cursor.execute("SELECT COUNT(*) FROM historial_vacunacion")
        print(f"  - Vacunaciones: {cursor.fetchone()[0]}")
        cursor.execute("SELECT COUNT(*) FROM pesajes")
        print(f"  - Pesajes: {cursor.fetchone()[0]}")
        cursor.execute("SELECT COUNT(*) FROM alimentacion")
        print(f"  - Alimentación: {cursor.fetchone()[0]}")

if __name__ == "__main__":
    insertar_datos()
