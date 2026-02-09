from django.shortcuts import redirect, render
from app import models
from app.forms import TaskForm

# Create your views here.

def home(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home') # Recarga la página para ver la nueva tarea
    else:
        form = TaskForm()

    tasks = models.Task.objects.all().order_by('-created_at')
    return render(request, 'index.html', {
        'tasks': tasks,
        'form': form
    })