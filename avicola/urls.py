from django.urls import path
from . import views

app_name = 'avicola'

urlpatterns = [
    path('', views.lista_aves, name='lista_aves'),
    path('registrar/', views.registrar_ave, name='registrar_ave'),
]
