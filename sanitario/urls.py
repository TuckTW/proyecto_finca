from django.urls import path
from . import views

app_name = 'sanitario'

urlpatterns = [
    path('', views.listar_vacunas, name='listar_vacunas'),
    path('vacunas/', views.listar_vacunas, name='listar_vacunas'),
    path('vacunas/registrar/', views.registrar_vacunacion, name='registrar_vacunacion'),
    path('vacunas/editar/<int:id>/', views.editar_vacunacion, name='editar_vacunacion'),
    path('vacunas/eliminar/<int:id>/', views.eliminar_vacunacion, name='eliminar_vacunacion'),
    path('tratamientos/', views.listar_tratamientos, name='listar_tratamientos'),
    path('tratamientos/registrar/', views.registrar_tratamiento, name='registrar_tratamiento'),
]
