from django.db import models


class Prueba(models.Model):
    titulo = models.CharField(max_length=100)
    subtitulo = models.CharField(max_length=100)
    cantidad = models.IntegerField()


# retorna el valor que deseemos del modelo, en este caso retornamos titulo y subtitulo
    def __str__(self):
        return self.titulo + '-' + self.subtitulo