from django.db import models
from ganado.models import Ganado

class Vacuna(models.Model):
    id_vacuna = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=80)
    descripcion = models.TextField(blank=True, null=True)
    dosis = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'vacunas'
        managed = False

    def __str__(self):
        return self.nombre

class HistorialVacunacion(models.Model):
    id_historial = models.AutoField(primary_key=True)
    id_ganado = models.ForeignKey(Ganado, on_delete=models.CASCADE, db_column='id_ganado')
    id_vacuna = models.ForeignKey(Vacuna, on_delete=models.RESTRICT, db_column='id_vacuna')
    id_usuario = models.IntegerField()
    fecha = models.DateField()
    proxima_fecha = models.DateField(null=True, blank=True)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'historial_vacunacion'
        managed = False

class Enfermedad(models.Model):
    id_enfermedad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=80)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'enfermedades'
        managed = False

    def __str__(self):
        return self.nombre

class Tratamiento(models.Model):
    id_tratamiento = models.AutoField(primary_key=True)
    id_ganado = models.ForeignKey(Ganado, on_delete=models.CASCADE, db_column='id_ganado')
    id_enfermedad = models.ForeignKey(Enfermedad, on_delete=models.RESTRICT, db_column='id_enfermedad')
    id_usuario = models.IntegerField()
    medicamento = models.CharField(max_length=80, blank=True, null=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'tratamientos'
        managed = False