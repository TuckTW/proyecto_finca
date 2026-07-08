from datetime import date

def calcular_recomendaciones_vacunas(animal):
    if not animal.fecha_nacimiento or animal.estado != 'Activo':
        return []

    dias_vida = (date.today() - animal.fecha_nacimiento).days
    meses_vida = dias_vida / 30.41

    recomendaciones = []

    if meses_vida >= 3:
        recomendaciones.append({
            'nombre': 'Fiebre Aftosa',
            'tipo': 'Obligatoria',
            'badge_color': 'bg-danger',
            'indicacion': 'Aplicar dosis de control semestral obligatoria (Proxima campana).'
        })

    if animal.sexo == 'Hembra' and 3 <= meses_vida <= 8:
        recomendaciones.append({
            'nombre': 'Brucelosis Bovina (Cepa 19 / RB51)',
            'tipo': 'Critica (Solo Hembras)',
            'badge_color': 'bg-purple text-white',
            'indicacion': 'Edad ideal de vacunacion (3-8 meses) para la proteccion del hato reproductivo.'
        })

    if meses_vida >= 4:
        recomendaciones.append({
            'nombre': 'Triple Bovina (Carbon/Septicemia/Edema)',
            'tipo': 'Sugerida',
            'badge_color': 'bg-primary',
            'indicacion': 'Prevencion de muerte subita por clostridiosis. Revacunar anualmente.'
        })

    if meses_vida >= 6:
        recomendaciones.append({
            'nombre': 'Rabia Silvestre',
            'tipo': 'Preventiva',
            'badge_color': 'bg-secondary',
            'indicacion': 'Recomendado si hay presencia de murcielagos hematofagos en la zona.'
        })

    return recomendaciones
