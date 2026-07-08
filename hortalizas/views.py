from django.shortcuts import render, redirect
from .models import Cultivo
from .forms import CultivoForm
from dashboard.models import Notificacion

def lista_cultivos(request):
    cultivos = Cultivo.objects.all()
    return render(request, 'hortalizas/lista_cultivos.html', {'cultivos': cultivos})

def registrar_cultivo(request):
    if request.method == 'POST':
        form = CultivoForm(request.POST)
        if form.is_valid():
            cultivo = form.save()
            Notificacion.objects.create(
                usuario=request.user,
                titulo="Nuevo Cultivo",
                mensaje=f"Se ha registrado el cultivo: {cultivo.nombre}",
                tipo="Exito"
            )
            return redirect('hortalizas:lista_cultivos')
    else:
        form = CultivoForm()
    return render(request, 'hortalizas/registrar_cultivo.html', {'form': form})
