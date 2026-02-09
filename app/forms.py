from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_from', 'task_to', 'description', 'state']
        widgets = {
            'task_from': forms.TextInput(attrs={'class': 'form-control'}),
            'task_to': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'state': forms.Select(attrs={'class': 'form-select'}),
        }