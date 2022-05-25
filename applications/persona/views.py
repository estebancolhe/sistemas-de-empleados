from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView
from .models import Empleado
from .forms import EmpleadoForm

class InicioView(TemplateView):
    ''' Vista que carga la pagina de inicio '''
    template_name='inicio.html'

class ListAllEmpleado(ListView):
    template_name = 'persona/list_all.html'
    paginate_by = 4 # paginacion de a 4 elementos
    ordering = 'first_name'
    context_object_name='empleados'

    def get_queryset(self):
        palabra_clave = self.request.GET.get("kword",'')
        # __icontains me va a buscar por los  caracteres o la union de caracteres 
        # que pongamos en el buscador, ej: si pongo "jo", empieza a buscar por esas letras todos
        # los resultados que contengan "jo" 
        lista = Empleado.objects.filter(full_name__icontains=palabra_clave)
        return lista

class ListByAreaEmpleado(ListView):
    template_name = 'persona/list_by_area.html'
    context_object_name = 'empleados'
    # queryset le digo a django con que caracteristica en particular me devuelve una lista o consulta
    # "consultas al ORM 'personalizadas'"
    # en el queryset ponemos como condicion el filtro 'departamento__short_name' es porque...
    # como es una Foreingkey o tiene una relacion uno a muchos se debe acceder al campo 'departamento'...
    # del modelo 'Empleado' y ademas al campo por el que deseamos filtrar que está...
    # en el modelo Departamento
    # PEOR FORMA DE HACER LISTVIEW ***************
    '''
    queryset = Empleado.objects.filter(departamento__short_name='contabilidad')
    '''

    # UNA DE LAS FORMAS CORRECTAS DE HACER UN LISTVIEW *********
    # este metodo siempre retorna una lista
    # podemos sobreescribir el metodo 'get_queryset' a conveniencia
    # esta es la forma de hacer filtros quemados
    '''
    def get_queryset(self):
        lista = Empleado.objects.filter(departamento__short_name='contabilidad')
        return lista
        '''

    # esta es la forma de hacerlos dinamicos
    def get_queryset(self):
        area = self.kwargs['shortname']
        lista = Empleado.objects.filter(departamento__short_name=area)
        return lista


class ListByTrabajoEmpleado(ListView):
    template_name = 'persona/list_by_trabajo.html'
    
    def get_queryset(self):
        trabajo = self.kwargs['job']
        lista = Empleado.objects.filter(job=trabajo)
        return lista


class ListEmpleadosAdmin(ListView):
    template_name = 'persona/lista_empleados.html'
    paginate_by = 10
    ordering = 'first_name'
    context_object_name='empleados'
    model = Empleado


# como hacer ListView por medio de caja de texto
class ListEmpleadosByKword(ListView):
    template_name = 'persona/by_keyword.html'
    # me permite redefinir el nombre con el que se accedera a la lista resultado que retorna el ListView
    # es decir, ya no se accedera a la informacion con el 'object_list', sino con la variable 'empleados'
    # en este ejemplo
    context_object_name = 'empleados'

    def get_queryset(self):
        # request = son las solicitudes que se han enviado al servidor
        # GET = trae solicitudes de tipo GET
        # get = recupera por medio de un get el valor cuya identifacion sea keyword en este ejemplo
        palabra_clave = self.request.GET.get("keyword",'')
        lista = Empleado.objects.filter(first_name=palabra_clave)
        return lista

class ListHabilidadesEmpleado(ListView):
    template_name = 'persona/habilidades.html'
    context_object_name = 'habilidades'

    def get_queryset(self):
        # el get permite obtener solo un resultado y no un conjunto de resultados
        habilidad = self.kwargs['habilidad']
        empleado = Empleado.objects.get(id=habilidad)
        # ahora gracias a la linea anterior ya tengo recuperado un registro
        # quiero recuperar las habilidades de un registro, como es un campo con relacion
        # de muchos a muchos entonces el 'all()' me permite recuperar todas las habilidades
        # de ese registro en este ejemplo
        return empleado.habilidades.all()


class EmpleadoDetailView(DetailView):
    model = Empleado
    template_name = "persona/detail_empleado.html"

    # forma de sobreescribir un metodo para que realice algo mas que necesite
    def get_context_data(self, **kwargs):
        context = super(EmpleadoDetailView, self).get_context_data(**kwargs)
        # todo un proceso
        context['titulo'] = 'Empleado del mes'
        return context

# vista generica que ayuda a llamar un template html
class SuccessView(TemplateView):
    template_name = "persona/success.html"

class EmpleadoCreateView(CreateView):
    model = Empleado
    template_name = "persona/add.html"
    # el CreateView necesita un campo fields donde se le indica que datos solicitará al momento...
    # de crear un objeto nuevo del modelo, si se pone ('__all__')  solicitará todos los campos...
    # que tenga el modelo
    '''fields = ['first_name', 'last_name', 'job', 'departamento', 'habilidades','avatar',]'''
    form_class = EmpleadoForm # se comenta fields y se pone esta linea porque se creo un formulario...
    # donde estaran los campos del modelo
    # el success_url es otro campo necesario... 
    # el cual redireccionará a un template (sea otro o al mismo template) luego de guardar la informacion
    # cuando en el 'success_url' es igual a '.' quiere decir que redireccione al mismo template y no a otro
    # si estuviera success_url = '/success', redirecciona a otro template llamado success.html...
    # pero no es una buena practica
    # reverse_lazy() es una forma de llamar templates de manera dinamica
    # con reverse_lazy('persona_app:'), ya estoy dentro del conjunto de rutas de la app persona
    # con reverse_lazy('persona_app:correcto'), ya estoy accediendo a la ruta con name = 'correcto'...
    # de la app persona
    success_url = reverse_lazy('persona_app:empleados_admin')

    # estoy sobreescribiendo el metodo 'form_valid'...
    # recibe dos parametros, el self y el form ->(la informacion que se le envia desde el template)
    def form_valid(self, form):
        # logica del proceso
        # form.save() lo que hace es guardar en la BD la informacion enviada por el template
        # en este caso estoy almacenando esa informacion en la variable 'empleado' y en la BD

        # commit=False me permite crer la instancia para empleado sin guardar el registro en la BD...
        # para este ejemplo, mas adelante concateno nombre y apellido...
        # y ahí si guardo el registro completo esto con la intencion de no realizar doble guardado...
        # cuando en el ultimo .save() lo puedo guardar completo
        empleado = form.save(commit=False)
        # se concatena el nombre con el apellido y con el metodo save de la instancia de empleado...
        # se procede a guardar en el campo full_name de la BD la informacion correspondiente
        # CONTEXTO: se necesita concatenar el nombre y el apellido, el formulario...
        # solicita nombre y apellido por separado, entonces se guardan los datos en la BD...
        # de manera separada, por alguna razon se necesitan juntos...
        # entonces para eso es todo este metodo de form_valid()
        empleado.full_name = empleado.first_name + ' ' + empleado.last_name
        empleado.save()
        # el super("nombre de la clase", self) es para decirle a django...
        # que estoy sobreescribiendo un metodo solo para la clase EmpleadoCreateView
        # se entra al metodo form_valid() solo cuando los datos enviados desde el template son validos
        return super(EmpleadoCreateView, self).form_valid(form)


class EmpleadoUpdateView(UpdateView):
    template_name = "persona/update.html"
    model = Empleado
    fields = ['first_name','last_name','job','departamento','habilidades',]
    success_url = reverse_lazy('persona_app:empleados_admin')

    # con  CreateView y con UpdateView se pueden sobreescribir los metodos de post() y...
    # form_valid(), el metodo post() sirve para hacer algun proceso previo antes del...
    # guardado de datos, en este caso almacenará algo antes de validar los datos...
    # con el form_valid()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # el request.POST es lo mismo que es request.data, tiene la informacion que se envia...
        # desde le template, por medio de request.POST obtengo todos los datos y como en un diccionario...
        # puedo obtener datos individuales accediendo a su clave...
        # ej: request.POST['clave_del_diccionario']
        print(request.POST['last_name'])
        return super().post(request, *args, **kwargs)

    def form_valid(self,form):

        return super(EmpleadoUpdateView, self).form_valid(form)


class EmpleadoDeleteView(DeleteView):
    model = Empleado
    template_name = "persona/delete.html"
    success_url = reverse_lazy('persona_app:empleados_admin')