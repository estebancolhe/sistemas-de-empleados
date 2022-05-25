from applications.home.models import Prueba
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView
from .models import Prueba
from .forms import PruebaForm

class PruebaView(TemplateView):
    template_name = 'home/prueba.html'


class ResumenFoundationView(TemplateView):
    template_name = 'home/resumen_foundation.html'


class PruebaListView(ListView):
    # la vista recibe un parametro "ListView" el cual tiene el valor del queryset
    # para imprimir el valor del queryset se utiliza un context_object_name y el nombre de esa variable
    # es el que se imprime en el HTML 
    template_name = "home/lista.html"
    context_object_name = 'listaNumeros'
    queryset = ['0','10', '20','30']


class ListarPrueba(ListView):
    template_name = "home/lista_prueba.html"
    model = Prueba
    context_object_name = 'lista'


class PruebaCreateView(CreateView):
    template_name = "home/add.html"
    model = Prueba
    # con form_class conectamos el formulario con el modelo
    form_class = PruebaForm
    success_url = '/'