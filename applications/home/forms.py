from django import forms
from .models import Prueba

class PruebaForm(forms.ModelForm):

    class Meta:
        # el formulario necesita saber con que campo va a trabajar, es por esto...
        # que se define el 'model'
        model = Prueba
        fields = (
            'titulo',
            'subtitulo',
            'cantidad',
        )
        # con widgets podemos personalizar los campos del form
        widgets = {
            'titulo':forms.TextInput(
                attrs={
                    'placeholder':'Ingrese titulo aqui'
                }
            )
        }

    def clean_cantidad(self):
        # se desea saber que informacio se ingresó en el campo 'cantidad'
        # para hacerlo se hace con self.cleaned_data['nombre_del_campo'], asi es como...
        # se recupera informacion del campo

        # si se desea realizar validaciones de los formularios, lo mejor es hacerlo en...
        # los fomularios directamente para optimizar el codigo y como buena practica
        cantidad = self.cleaned_data['cantidad']
        if cantidad < 10:
            raise forms.ValidationError('Ingrese un numero mayor a 10')
        return cantidad