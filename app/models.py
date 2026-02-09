from django.db import models

# Create your models here.

class Task(models.Model):
    task_from = models.CharField(max_length=255)
    task_to = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    state = models.CharField(
        max_length=2,
        choices=[
            ('P', 'Pendiente'),
            ('C', 'Completado'),
            ('E', 'En espera'),
        ],
        default='P'
    )

    def __str__(self):
        return self.task_from + ' - ' + self.task_to

    def get_status_color(self):
        if self.state == 'C':
            return 'success'  
        elif self.state == 'E':
            return 'primary' 
        else:
            return 'warning'  
    