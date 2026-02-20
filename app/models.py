from django.db import models

# Create your models here.

class Procesos(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Task(models.Model):
    reportado_por = models.CharField(max_length=255)
    proceso = models.ForeignKey(Procesos, on_delete=models.CASCADE)
    priority = models.CharField(max_length=2,
        choices=[
            ('B', 'Baja'),
            ('M', 'Media'),
            ('A', 'Alta'),
        ],
        default='M'
    )
    created_at = models.DateTimeField(auto_now_add=True)
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
    descripcion = models.TextField()
    solucion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.reportado_por + ' - ' + self.proceso.nombre

    def get_status_color(self):
        if self.state == 'C':
            return 'success'  
        elif self.state == 'E':
            return 'primary' 
        else:
            return 'warning'  
    
    def get_state_display(self):
        return dict(self._meta.get_field('state').choices).get(self.state, 'Desconocido')
    
    def get_priority_color(self):
        if self.priority == 'A':
            return 'danger'   # Rojo para Alta
        elif self.priority == 'M':
            return 'warning'  # Amarillo para Media
        elif self.priority == 'B':
            return 'info'     # Azul/Cian para Baja
        return 'secondary'

    # Ya que Django trae un método automático, puedes usar este o el nativo
    def get_priority_label(self):
        return dict(self._meta.get_field('priority').choices).get(self.priority, 'N/A')