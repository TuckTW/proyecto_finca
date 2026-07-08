from django import forms
from .models import LoteAves

class LoteAvesForm(forms.ModelForm):
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Enfermo/Cuarentena', 'Enfermo / Cuarentena'),
        ('Vendido', 'Vendido'),
        ('Finalizado', 'Finalizado'),
    ]

    estado = forms.ChoiceField(
        choices=ESTADO_CHOICES,
        initial='Activo',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = LoteAves
        fields = ['codigo', 'tipo_ave', 'cantidad_inicial', 'cantidad_actual', 'fecha_ingreso', 'estado']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: LOT-001'}),
            'tipo_ave': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Ponedoras, Engorde'}),
            'cantidad_inicial': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'cantidad_actual': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
