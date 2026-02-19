from django.contrib import admin
from django.urls import path

from app.views import completar_tarea, home

urlpatterns = [
    path('home/', home, name='home'),
    path('completar_tarea/<int:task_id>/', completar_tarea, name='completar_tarea'),
]