from django.shortcuts import render, redirect
from .models import LoteAves
from .forms import LoteAvesForm
from dashboard.models import Notificacion

def lista_aves(request):
    lotes = LoteAves.objects.all()
    return render(request, 'avicola/lista_aves.html', {'lotes': lotes})

def registrar_ave(request):
    if request.method == 'POST':
        form = LoteAvesForm(request.POST)
        if form.is_valid():
            lote = form.save()
            Notificacion.objects.create(
                usuario=request.user,
                titulo="Nuevo Lote Avicola",
                mensaje=f"Se ha registrado un nuevo lote: {lote.codigo}",
                tipo="Exito"
            )
            return redirect('avicola:lista_aves')
    else:
        form = LoteAvesForm()
    return render(request, 'avicola/registrar_ave.html', {'form': form})
