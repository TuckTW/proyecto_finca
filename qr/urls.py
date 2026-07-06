from django.urls import path
from . import views

app_name = 'qr'

urlpatterns = [
    path('', views.index, name='index'),
    path('generar/<int:id>/', views.generar_qr, name='generar_qr'),
    path('escanear/<str:codigo>/', views.escanear_qr, name='escanear_qr'),
]
