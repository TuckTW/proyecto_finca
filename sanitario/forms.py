from django import forms
from .models import Vacuna, HistorialVacunacion, Enfermedad, Tratamiento
from ganado.models import Ganado

class VacunacionForm(forms.ModelForm):
    class Meta:
        model = HistorialVacunacion
        fields = ['id_ganado', 'id_vacuna', 'fecha', 'proxima_fecha', 'observaciones']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'proxima_fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'id_ganado': forms.Select(attrs={'class': 'form-control'}),
            'id_vacuna': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_ganado'].queryset = Ganado.objects.filter(estado='Activo')
        self.fields['id_ganado'].label = 'Animal'
        self.fields['id_vacuna'].queryset = Vacuna.objects.all()
        self.fields['id_vacuna'].label = 'Vacuna'
        self.fields['fecha'].label = 'Fecha de Aplicacion'

class TratamientoForm(forms.ModelForm):
    class Meta:
        model = Tratamiento
        fields = ['id_ganado', 'id_enfermedad', 'medicamento', 'fecha_inicio', 'fecha_fin', 'observaciones']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'id_ganado': forms.Select(attrs={'class': 'form-control'}),
            'id_enfermedad': forms.Select(attrs={'class': 'form-control'}),
            'medicamento': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_ganado'].queryset = Ganado.objects.all()
        self.fields['id_ganado'].label = 'Animal'
        self.fields['id_enfermedad'].queryset = Enfermedad.objects.all()
        self.fields['id_enfermedad'].label = 'Enfermedad'
