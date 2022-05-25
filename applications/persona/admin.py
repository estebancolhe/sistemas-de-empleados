from django.contrib import admin
from .models import Empleado, Habilidades

# Registramos los modelos para que puedan aparecer en el admin de Django


admin.site.register(Habilidades)

# Esta configuracion sirve para listar la informacion en el admin de manera organizada...
# ej. como en una base de datos, traer los campos en las columnas y los datos en las filas
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'departamento',
        'job',
        'full_name',
    )

    # si se quiere agregar un campo para visulizar en el admin y el campo no está en la BD...
    # se agrega de igual manera en el "list_display" y se realiza la funcion...
    # que traiga la informacion que se quiere mostrar en el campo, ej full_name
    # con el parametro "obj" pasamos una funcion extra
    def full_name(self, obj):
        #Toda la logica del metodo, en este caso un print para poner algo
        print(obj.first_name)
        # el return de la funcion es con lo que llenará las tablas del campo
        return obj.first_name + ' ' + obj.last_name

    # esto hace que el admin tenga un buscador dependiendo del campo que se ponga, ej: first_name
    search_fields = ('first_name',)

    # me permite filtrar informacion dependiendo del campo que elija, ej: job
    list_filter = ('departamento', 'job', 'habilidades')

    # campo para seleccionar informacion de manera horizontal y solo sirve para los campos con relacion...
    # muchos a muchos
    filter_horizontal = ('habilidades',)

admin.site.register(Empleado, EmpleadoAdmin)