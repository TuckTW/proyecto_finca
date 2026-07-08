from django.db import models
from datetime import date

class Raza(models.Model):
    id_raza = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'razas'
        managed = False

    def __str__(self):
        return self.nombre

class Ganado(models.Model):
    SEXO_CHOICES = [
        ('Macho', 'Macho'),
        ('Hembra', 'Hembra'),
    ]
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Enfermo', 'Enfermo'),
        ('Vendido', 'Vendido'),
        ('Muerto', 'Muerto'),
    ]

    id_ganado = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=50)
    id_raza = models.ForeignKey(Raza, on_delete=models.RESTRICT, db_column='id_raza')
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    peso_inicial = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    peso_actual = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Activo')
    color = models.CharField(max_length=30, blank=True, null=True)
    foto = models.CharField(max_length=255, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ganado'
        managed = False

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    def calcular_gmd(self):
        """Calcula la Ganancia Media Diaria (GMD) en kg."""
        if self.peso_inicial and self.peso_actual and self.fecha_nacimiento:
            dias = (date.today() - self.fecha_nacimiento).days
            if dias > 0:
                return float((self.peso_actual - self.peso_inicial) / dias)
        return 0.0

    def predecir_peso(self, dias_a_futuro=30):
        """Predice el peso estimado en N dias."""
        gmd = self.calcular_gmd()
        if gmd > 0 and self.peso_actual:
            peso_estimado = float(self.peso_actual) + (gmd * dias_a_futuro)
            return round(peso_estimado, 2)
        return self.peso_actual or 0.0

class CodigoQR(models.Model):
    id_qr = models.AutoField(primary_key=True)
    id_ganado = models.OneToOneField(Ganado, on_delete=models.CASCADE, db_column='id_ganado')
    codigo_qr = models.CharField(max_length=150, unique=True)
    fecha_generacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'codigo_qr'
        managed = False
