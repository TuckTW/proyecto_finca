from django import forms
from .models import Alimentacion, Pesaje
from ganado.models import Ganado

class AlimentacionForm(forms.ModelForm):
    class Meta:
        model = Alimentacion
        fields = ['id_ganado', 'tipo_alimento', 'cantidad', 'fecha']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'id_ganado': forms.Select(attrs={'class': 'form-control'}),
            'tipo_alimento': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_ganado'].queryset = Ganado.objects.filter(estado='Activo')
        self.fields['id_ganado'].label = 'Animal'
        self.fields['tipo_alimento'].label = 'Tipo de Alimento'
        self.fields['cantidad'].label = 'Cantidad (kg)'

class PesajeForm(forms.ModelForm):
    class Meta:
        model = Pesaje
        fields = ['id_ganado', 'fecha', 'peso', 'observaciones']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'id_ganado': forms.Select(attrs={'class': 'form-control'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'observaciones': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_ganado'].queryset = Ganado.objects.all()
        self.fields['id_ganado'].label = 'Animal'
        self.fields['peso'].label = 'Peso (kg)'
