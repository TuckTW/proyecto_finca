from django import forms
from .models import Ganado, Raza

class GanadoForm(forms.ModelForm):
    class Meta:
        model = Ganado
        fields = ['codigo', 'nombre', 'id_raza', 'sexo', 'fecha_nacimiento',
                  'peso_inicial', 'estado', 'color', 'observaciones']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: BHM001'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'id_raza': forms.Select(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'peso_inicial': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_raza'].queryset = Raza.objects.all()
        self.fields['id_raza'].label = 'Raza'
        self.fields['peso_inicial'].label = 'Peso Inicial (kg)'

class GanadoBusquedaForm(forms.Form):
    codigo = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Codigo'}))
    nombre = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}))
    raza = forms.ModelChoiceField(queryset=Raza.objects.all(), required=False,
                                   widget=forms.Select(attrs={'class': 'form-control'}), label='Raza')
    sexo = forms.ChoiceField(choices=[('', 'Todos')] + Ganado.SEXO_CHOICES, required=False,
                            widget=forms.Select(attrs={'class': 'form-control'}), label='Sexo')
    estado = forms.ChoiceField(choices=[('', 'Todos')] + Ganado.ESTADO_CHOICES, required=False,
                              widget=forms.Select(attrs={'class': 'form-control'}), label='Estado')
    peso_min = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Minimo'}))
    peso_max = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Maximo'}))
