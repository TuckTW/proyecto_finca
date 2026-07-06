from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    path('', views.index, name='index'),
    path('pdf/', views.reporte_pdf, name='reporte_pdf'),
    path('excel/', views.reporte_excel, name='reporte_excel'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),
]
