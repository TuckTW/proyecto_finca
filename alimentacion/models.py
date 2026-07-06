from django.db import models
from ganado.models import Ganado

class Alimentacion(models.Model):
    id_alimentacion = models.AutoField(primary_key=True)
    id_ganado = models.ForeignKey(Ganado, on_delete=models.CASCADE, db_column='id_ganado')
    id_usuario = models.IntegerField()
    tipo_alimento = models.CharField(max_length=80, blank=True, null=True)
    cantidad = models.DecimalField(max_digits=8, decimal_places=2)
    fecha = models.DateField()

    class Meta:
        db_table = 'alimentacion'
        managed = False

class Pesaje(models.Model):
    id_pesaje = models.AutoField(primary_key=True)
    id_ganado = models.ForeignKey(Ganado, on_delete=models.CASCADE, db_column='id_ganado')
    id_usuario = models.IntegerField()
    fecha = models.DateField()
    peso = models.DecimalField(max_digits=8, decimal_places=2)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'pesajes'
        managed = False