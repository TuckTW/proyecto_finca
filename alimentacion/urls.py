from django.urls import path
from . import views

app_name = 'alimentacion'

urlpatterns = [
    path('', views.listar_alimentacion, name='listar_alimentacion'),
    path('registrar/', views.registrar_alimentacion, name='registrar_alimentacion'),
    path('editar/<int:id>/', views.editar_alimentacion, name='editar_alimentacion'),
    path('eliminar/<int:id>/', views.eliminar_alimentacion, name='eliminar_alimentacion'),
    path('pesajes/', views.listar_pesajes, name='listar_pesajes'),
    path('pesajes/registrar/', views.registrar_pesaje, name='registrar_pesaje'),
]
