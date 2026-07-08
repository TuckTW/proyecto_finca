from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('notificaciones/leer/', views.marcar_notificaciones_leidas, name='marcar_leidas'),
]
