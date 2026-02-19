from django.shortcuts import get_object_or_404, redirect, render
from app import models
from app.forms import TaskForm

# Create your views here.

def home(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home') 
    else:
        form = TaskForm()

    tasks = models.Task.objects.all().order_by('-created_at')
    return render(request, 'index.html', {
        'tasks': tasks,
        'form': form
    })

def completar_tarea(request, task_id):
    task = get_object_or_404(models.Task, id=task_id)
    task.state = 'C' 
    task.save()
    return redirect('home')