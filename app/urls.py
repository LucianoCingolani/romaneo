from django.contrib import admin
from django.urls import path

from app.views import completar_tarea, exportar_tareas_csv, exportar_tareas_pdf, home, agregar_solucion

urlpatterns = [
    path('', home, name='home'),
    path('completar_tarea/<int:task_id>/', completar_tarea, name='completar_tarea'),
    path('solucion/<int:task_id>/', agregar_solucion, name='agregar_solucion'),
    path('exportar-csv/', exportar_tareas_csv, name='exportar_tareas_csv'),
    path('exportar-pdf/', exportar_tareas_pdf, name='exportar_tareas_pdf'),
]