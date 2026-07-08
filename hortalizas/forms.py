from django import forms
from .models import Cultivo

class CultivoForm(forms.ModelForm):
    ESTADO_CHOICES = [
        ('Preparacion', 'Preparacion de suelo'),
        ('Siembra', 'Siembra/Plantacion'),
        ('Crecimiento', 'En Crecimiento'),
        ('Cosecha', 'En Cosecha'),
        ('Finalizado', 'Finalizado/Perdido'),
    ]

    estado = forms.ChoiceField(
        choices=ESTADO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Cultivo
        fields = '__all__'
        widgets = {
            'fecha_siembra': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'area_asignada': forms.TextInput(attrs={'class': 'form-control'}),
        }
