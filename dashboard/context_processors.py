from .models import Notificacion

def lista_notificaciones(request):
    if request.user.is_authenticated:
        notificaciones_sin_leer = Notificacion.objects.filter(usuario=request.user, leido=False)[:5]
        cantidad_sin_leer = Notificacion.objects.filter(usuario=request.user, leido=False).count()
        return {
            'notificaciones_globales': notificaciones_sin_leer,
            'cantidad_notificaciones': cantidad_sin_leer
        }
    return {}
