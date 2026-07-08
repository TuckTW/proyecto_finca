from django.db import models

class LoteAves(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    tipo_ave = models.CharField(max_length=50)
    cantidad_inicial = models.IntegerField()
    cantidad_actual = models.IntegerField()
    fecha_ingreso = models.DateField()
    estado = models.CharField(max_length=30, default='Activo')

    def __str__(self):
        return f"{self.codigo} - {self.tipo_ave}"

class AlimentacionAves(models.Model):
    lote = models.ForeignKey(LoteAves, on_delete=models.CASCADE)
    tipo_alimento = models.CharField(max_length=100)
    cantidad_kg = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()

class Mortalidad(models.Model):
    lote = models.ForeignKey(LoteAves, on_delete=models.CASCADE)
    cantidad_bajas = models.IntegerField()
    causa = models.TextField(blank=True, null=True)
    fecha = models.DateField()
