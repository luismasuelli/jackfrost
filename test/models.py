#coding: utf-8
from django.db import models
from jackfrost.fields import AutocompleteCharField, AutocompleteModelChoiceField, AutocompleteModelMultipleChoiceField

class Language(models.Model):
    name = models.CharField(max_length=50, null=False)

    def __unicode__(self):
        return self.name

class Group(models.Model):
    description = models.CharField(max_length=255, null=False)

    def __unicode__(self):
        return self.description

class Speaker(models.Model):
    #estos campos buscaran autocompletar en los
    #mismos campos de entradas ya existentes
    #(autocompletar de texto)
    name = models.CharField(max_length=50, null=False)
    #este campo buscara en una referencia multiple
    languages = models.ManyToManyField(Language, related_name='speakers')
    #este campo buscara en una referencia simple
    group = models.ForeignKey(Group, null=False)

    def __unicode__(self):
        return self.name

#podemos crear un formulario de modelo o un formulario normal, pero si usamos controles
#con autocompletar nuestro formulario debe ser tipo AutocompleteForm en lugar de Form,
#o bien AutocompleteModelForm en lugar de ModelForm. esto nos permite ciertos metodos
#para incluir media de jquery e incluso cambiar tematicas.
#
#cuando creamos nuestro formulario para el modelo, es importante recalcar que los campos
#que queremos que sean de Autocompletar tengan ese tipo de campo. en tal momento tenemos
#que asegurarnos de especificarle como uno de los parametros el nombre de la fuente de
#valores para el autocompletar cuando se ejecute desde el lado cliente.
#
#es importante tener presente, no a modo obligatorio sino a modo de utilidad, que si
#usamos un campo AutocompleteCharField (para obtener ùnicamente el texto y no un objeto
#de modelo como referencia) debería la fuente de ese campo ser un modelo cuyo valor
#convertido a cadena sea el mismo valor del campo. ejemplo: si queremos en nuestro
#formulario de modelo para la tabla T editar un determinado campo C mediante un control
#de autocompletar de texto (AutocompleteCharField), el metodo __unicode__ de la tabla
#T debería devolver el valor de C, para que coincida. esto es útil para reutilizar
#valores anteriores.
#
#otra cosa es que los campos que serán listados están preparados para actuar con su
#widget predeterminado, por lo que asignarles otro widget será totalmente ignorado.
#
#los campos AC que podemos usar son los siguientes:
#
#  AutocompleteCharField : un campo de texto con capacidad de autocompletar.
#    parametros de constructor:
#    1. lookup_name = el nombre del lookup que hayamos definido como se explica en urls.py
#    *args, **kwargs: los necesarios para el CharField de django (form fields).
#
#  AutocompleteModelChoiceField : un campo de referencia N:1 con capacidad de autocompletar.
#    parametros de constructor:
#    1. lookup_name = el nombre del lookup que hayamos definido como se explica en urls.py
#    *args, **kwargs: los necesarios para el Field de django (form fields).
#
#  AutocompleteModelMultipleChoiceField: un campo de referencia N:N con capacidad de autocompletar
#    cada una de las opciones que son buscadas. un control html de lista acumula las opciones
#    mientras que un hidden realmente es quien acumula los valores para enviar al servidor.
#    parametros del constructor:
#    1. lookup_name = el nombre del lookup que hayamos definido como se explica en urls.py
#    *args, **kwargs: los necesarios para el Field de django (form fields).
#
#otro tema sumamente importante: cuando vayamos a validar un campo que tenga autocompletares,
#y mas que nada los que son referenciantes (simples o multiples), tenemos que invocar con
#anterioridad al metodo AutocompleteField.set_request_in_each_field(form, request) sobre
#el formulario y pasando la peticion http actual. de otra forma la validacion no funcionará
#(y peor aun: provocará excepciones si es que hay funciones filtro que la usan o funciones
#de control de error 403 o 404 que la consultan (ver urls.py para mas detalles)).


class SpeakerForm(models.forms.ModelForm):

    name = AutocompleteCharField('test_app.speakers')
    group = AutocompleteModelChoiceField('test_app.groups', widget_attrs={'before_set': 'ss_before_set', 'after_set':'ss_after_set', 'before_del': 'ss_before_del', 'after_del': 'ss_after_del', 'renderer': 'ss_render'})
    languages = AutocompleteModelMultipleChoiceField('test_app.languages', widget_attrs={'before_add': 'ms_before_add', 'after_add': 'ms_after_add', 'before_rem': 'ms_before_rem', 'after_rem': 'ms_after_rem', 'renderer': 'ms_render'})

    class Meta:
        model = Speaker
