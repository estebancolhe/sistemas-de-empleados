from django.db import models

class Departamento(models.Model):
    name = models.CharField('Nombre',max_length=50)
    short_name = models.CharField('Nombre Corto',max_length=20, unique=True)
    anulate=models.BooleanField('Anulado', default=False)

    class Meta:
        # Se establece el nombre en singular
        verbose_name = 'Mi Departamento'
        # se establece el nombre cuando se muestre informacion en plural
        verbose_name_plural = 'Areas de la Empresa'
        # se establece la manera en la cual quiero que django me ordene la informacion, ej. por nombre
        # si quiero que la informacion se muestre en orden inverso seria asi...
        # ordering = ['-name']
        ordering = ['name']
        # sirve para evitar que se registre una combinacion que ya existe, ej. que no se guarden...
        # registros con el mismo nombre y short_name 
        unique_together = ('name', 'short_name')

    def __str__(self):
        return str(self.id) + '-' + self.name + '-' + self.short_name