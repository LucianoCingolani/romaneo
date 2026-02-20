from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['reportado_por', 'proceso', 'descripcion', 'state', 'priority']
        widgets = {
            'reportado_por': forms.TextInput(attrs={'class': 'form-control'}),
            'proceso': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'state': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
        }