from applications.departamento.forms import NewDepartamentoForm
from django.shortcuts import render
from django.views.generic.edit import FormMixin, FormView
from django.views.generic import ListView
from applications.persona.models import Empleado
from .models import Departamento
from .forms import NewDepartamentoForm

class DepartamentoListView(ListView):
    template_name = "departamento/lista.html"
    model = Departamento
    context_object_name = "departamentos"

# como vamos a trabajar con un formulario que no es basado en modelos, necesitamos la vista generica...
# 'FormView'
class NewDepartamentoView(FormView):
    template_name = 'departamento/new_departamento.html'
    form_class = NewDepartamentoForm
    success_url = '/'

    def form_valid(self, form):
        print('****** Estamos en el form valid ******')
        # en este metodo estamos creando un departamento con algunos datos de un empleado

        # como departamento es una clave foranea no se puede guardar la informacion de la misma manera...
        # que first_name, last_name, job, se debe de crear una instancia de la clase como a continuacion
        depa = Departamento(
            name=form.cleaned_data['departamento'],
            short_name=form.cleaned_data['shortname']
        )
        depa.save()

        # Con form.cleaned_data['nombre del campo'] es como recuperamos los datos que van...
        # en las cajas de texto de los formularios
        nombre = form.cleaned_data['nombre']
        apellido = form.cleaned_data['apellido']
        # asi es una forma de crear un objeto con el ORM en el modelo Empleado
        Empleado.objects.create(
            first_name=nombre,
            last_name=apellido,
            job='1',
            departamento =  depa
        )
        return super(NewDepartamentoView, self).form_valid(form)