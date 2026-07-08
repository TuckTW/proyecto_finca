from django.db import models

class Cultivo(models.Model):
    nombre = models.CharField(max_length=100)
    area_asignada = models.CharField(max_length=50)
    fecha_siembra = models.DateField()
    estado = models.CharField(max_length=50, default='En proceso')

    def __str__(self):
        return f"{self.nombre} - {self.area_asignada}"

class FaseProceso(models.Model):
    cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE)
    nombre_fase = models.CharField(max_length=50)
    fecha_inicio = models.DateField()
    observaciones = models.TextField(blank=True, null=True)

class Cosecha(models.Model):
    cultivo = models.ForeignKey(Cultivo, on_delete=models.CASCADE)
    fecha_cosecha = models.DateField()
    cantidad_kg = models.DecimalField(max_digits=10, decimal_places=2)
    calidad = models.CharField(max_length=50)
