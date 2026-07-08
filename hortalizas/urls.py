from django.urls import path
from . import views

app_name = 'hortalizas'

urlpatterns = [
    path('', views.lista_cultivos, name='lista_cultivos'),
    path('registrar/', views.registrar_cultivo, name='registrar_cultivo'),
]
