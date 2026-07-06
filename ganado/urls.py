from django.urls import path
from . import views

app_name = 'ganado'

urlpatterns = [
    path('', views.listar_ganado, name='listar_ganado'),
    path('registrar/', views.registrar_ganado, name='registrar_ganado'),
    path('editar/<int:id>/', views.editar_ganado, name='editar_ganado'),
    path('eliminar/<int:id>/', views.eliminar_ganado, name='eliminar_ganado'),
    path('buscar/', views.buscar_ganado, name='buscar_ganado'),
]
