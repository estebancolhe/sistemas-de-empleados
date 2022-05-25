from django.db import models
from applications.departamento.models import Departamento
from ckeditor.fields import RichTextField


class Habilidades(models.Model):
    habilidad = models.CharField('Habilidad', max_length=50)

    class Meta:
        verbose_name = 'Habilidad'
        verbose_name_plural = 'Habilidades Empleados'

    def __str__(self):
        return str(self.id) + '-' + self.habilidad



class Empleado(models.Model):
    JOB_CHOICES = (
        ('0', 'Contador'),
        ('1', 'Administrador'),
        ('2', 'Economista'),
        ('3','Otro'),
    )
    first_name = models.CharField('Nombres',max_length=60)
    last_name = models.CharField('Apellido', max_length=60)
    full_name = models.CharField('Nombres completos', max_length=120, blank=True)
    job = models.CharField('Trabajo',max_length=1,choices=JOB_CHOICES)
    # el campo "departamento" esta programado para relacion de 1 a muchos
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='empleado', blank=True, null=True)
    # el campo habilidades tiene relacion de muchos a muchos
    habilidades = models.ManyToManyField(Habilidades)
    # instalo una app de terceros ckeditor, importo el RichTextField y lo agrego como un campo en la BD
    # agrego la app en settings en "INSTALLED_APPS" y cuando reviso en admin, ya aparece el campo para...
    # crear texto
    hoja_vida = RichTextField()

    def __str__(self):
        return str(self.id) + '-' + self.first_name + '-' + self.last_name
    
    # Cuando quiero que solo se escoja un valor especifico de una lista especifica implementada por mi
    # Creo un objeto CHOICES con las opciones a escoger y luego en el campo del modelo
    # en la opcion de "choices" le doy el valor del objeto CHOICES

    class Meta:
        verbose_name = 'Mi Empleado'
        verbose_name_plural = 'Empleados de la empresa'
        ordering = ['-first_name', 'last_name']
        unique_together = ('first_name', 'departamento')