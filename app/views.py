from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from app import models
from app.forms import TaskForm
import csv
from django.utils import timezone
from django.template.loader import get_template
from xhtml2pdf import pisa

# Create your views here.

def home(request):
    lista_procesos = models.Procesos.objects.all()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TaskForm()

    # 1. Empezamos con todas las tareas
    tasks = models.Task.objects.all().order_by('-created_at')

    # 2. Capturamos los filtros desde la URL (GET)
    f_fecha = request.GET.get('fecha')
    f_proceso = request.GET.get('proceso')
    f_estado = request.GET.get('estado')

    # 3. Aplicamos los filtros de forma encadenada si existen
    if f_fecha:
        tasks = tasks.filter(created_at__date=f_fecha)
    
    if f_proceso:
        # 'icontains' para que busque parte del nombre sin importar mayúsculas
        tasks = tasks.filter(proceso=f_proceso)
    
    if f_estado:
        tasks = tasks.filter(state=f_estado)

    return render(request, 'index.html', {
        'tasks': tasks,
        'form': form,
        'lista_procesos': lista_procesos,
    })

def completar_tarea(request, task_id):
    task = get_object_or_404(models.Task, id=task_id)
    task.state = 'C' 
    task.save()
    return redirect('home')

def agregar_solucion(request, task_id):
    if request.method == 'POST':
        tarea = get_object_or_404(models.Task, id=task_id)
        tarea.solucion = request.POST.get('solucion_texto')
        tarea.save()
    return redirect('home') 

def exportar_tareas_csv(request):
    # 1. Aplicamos la misma lógica de filtrado que en tu vista 'home'
    tasks = models.Task.objects.all().order_by('-created_at')

    f_fecha = request.GET.get('fecha')
    f_proceso = request.GET.get('proceso')
    f_estado = request.GET.get('estado')

    if f_fecha:
        tasks = tasks.filter(created_at__date=f_fecha)
    if f_proceso:
        tasks = tasks.filter(proceso_id=f_proceso)
    if f_estado:
        tasks = tasks.filter(state=f_estado)

    # 2. Creamos el objeto de respuesta CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="reporte_tareas_{f_fecha or "general"}.csv"'
    
    # Manejo de caracteres especiales (acentos)
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    
    # Cabeceras
    writer.writerow(['ID', 'Fecha', 'Proceso', 'Reportado Por', 'Prioridad', 'Estado', 'Descripción', 'Solución'])

    # Datos
    for t in tasks:
        writer.writerow([
            t.id,
            t.created_at.strftime('%d/%m/%Y %H:%M'),
            t.proceso.nombre,
            t.reportado_por,
            t.get_priority_display(),
            t.get_state_display(),
            t.descripcion,
            t.solucion if t.solucion else "Sin solución"
        ])

    return response


def exportar_tareas_pdf(request):
    tasks = models.Task.objects.all().order_by('-created_at')
    
    f_fecha = request.GET.get('fecha')
    f_proceso = request.GET.get('proceso')
    f_estado = request.GET.get('estado')

    if f_fecha:
        tasks = tasks.filter(created_at__date=f_fecha)
    if f_proceso:
        tasks = tasks.filter(proceso_id=f_proceso)
    if f_estado:
        tasks = tasks.filter(state=f_estado)

    template_path = 'reporte_pdf.html'
    context = {
        'tasks': tasks,
        'hoy': timezone.now(),
    }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_{f_fecha or "general"}.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
       return HttpResponse('Ocurrió un error al generar el PDF', status=500)
    return response