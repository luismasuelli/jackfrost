#coding: utf-8
from django.conf.urls.defaults import patterns, include, url
from jackfrost import lookups
from views import *
from models import Speaker, Group, Language

lookups.register(
    r'^speakers-%s/$',       #.patron url (%s se reemplaza por one|many|ac, son 3 urls).
    'test_app.speakers',     #.cualquier nombre, debemos respetarlo.
    Speaker.objects.all(),   #.objeto de consulta de esos datos.
    None,                    #.filtro opcional con parametros (QuerySet, HttpRequest)
                             #cuyo resultado es otro QuerySet que sea producido por
                             #%1 y basandose en datos que se obtienen de %2.
                             #poniendo None no hay filtro.
    ('name',)                #.al menos un campo debe haber y tales deben ser
                             #visibles desde la query.
)

lookups.register(
    r'^languages-%s/$',      #.patron url (%s se reemplaza por one|many|ac, son 3 urls).
    'test_app.languages',    #.cualquier nombre, debemos respetarlo.
    Language.objects.all(),  #.objeto de consulta de esos datos.
    None,                    #.filtro opcional con parametros (QuerySet, HttpRequest)
                             #cuyo resultado es otro QuerySet que sea producido por
                             #%1 y basandose en datos que se obtienen de %2.
                             #poniendo None no hay filtro.
    ('name',)                #.al menos un campo debe haber y tales deben ser
                             #visibles desde la query.
)

lookups.register(
    r'^groups-%s/$',         #.patron url (%s se reemplaza por one|many|ac, son 3 urls).
    'test_app.groups',       #.cualquier nombre, debemos respetarlo.
    Group.objects.all(),     #.objeto de consulta de esos datos.
    None,                    #.filtro opcional con parametros (QuerySet, HttpRequest)
                             #cuyo resultado es otro QuerySet que sea producido por
                             #%1 y basandose en datos que se obtienen de %2.
                             #poniendo None no hay filtro.
    ('description',)         #.al menos un campo debe haber y tales deben ser
                             #visibles desde la query.
)

#registra un juego de vistas para cierto juego de datos que se accedan desde
#componentes basados en autocompletar. en front-end se usa el autocompletar
#de jqueryui, y la lista de elementos que se ve en los componentes autocompletar
#tienen una determinada clave (que se usara como valor) y el valor de convertir a
#unicode un objeto de modelo. es decir que para que quede bien la seleccion por
#autocompletar de instancias de una tabla de Django, en dicha tabla deberiamos
#definir el metodo __unicode__(self) y devolver lo que queramos mostrar.
#
#Parametros por orden y nombre:
#
#1. pattern: patron de url. debe ser una cadena con una unica ocurrencia
#   de la subcadena '%s'. tal subcadena es reemplazada 3 veces, y se crean
#   3 vistas. la cadena debe comenzar en ^ y terminar en $ si queremos que
#   sean urls definidas y no mascaras para otras urls que podriamos necesitar
#   ya que con esos 3 patrones accederemos a 3 vistas diferentes. ejemplo
#   para el caso del patron r'^mipatron-%s/$' dentro del espacio actual:
#       r'^mipatron-ac/$' : se crea una vista, para el juego de datos que queremos
#                           registrar, que nos permitira autocompletar desde el plugin
#                           de jquery de autocompletar.
#       r'^mipatron-one/$' : se crea una vista, para el juego de datos que queremos
#                            registrar, que nos permitira popular los datos iniciales
#                            para referencias simples (relaciones 1-N, un selector).
#       r'^mipatron-many/$' : se crea una vista, para el juego de datos que queremos
#                             registrar, que nos permitira popular los datos iniciales
#                             para referencias multiples (relaciones N-N, un selector
#                             multiple).
#
#2. name: un nombre que debe ser único. ese nombre lo usaremos para darle un nombre
#   a este lookup que estamos registrando. lo usaremos luego para obtenerlo. las vistas
#   tendran nombres internos para que puedan revertirse usando reverse. respectivamente
#   sus nombres seran  (name + '-ac'), (name + '-one') y (name + '-many').
#
#3. queryset: es la consulta base que compondra el juego de datos sobre el que queremos
#   hacer el autocompletar, obtener los datos iniciales, o incluso validar los datos
#   enviados al servidor para ese campo. normalmente es Tabla.objects.all() pero
#   tranquilamente puede ser cualquier otro queryset (siendo Tabla una clase que
#   descienta de models.Model).
#
#4. filter: es una funcion que toma dos parametros: el queryset especificado
#   en el parametro anterior, y la peticion http que se estè ejecutando en ese momento.
#   ese filtro se usa para limitar los datos a mostrar para la peticion http actual. su
#   valor devuelto es otro queryset creado a partir del primero, con los datos limitados.
#   si su valor es None, el queryset en el parametro anterior no es filtrado, sino que es
#   usado directamente.
#
#5. field_list: es una tupla no vacia de cadenas que son nombres de campos que deben
#   existir en el queryset que usemos. son los campos sobre los que se harà la bùsqueda,
#   retornando cada registro que contenga al menos una de las palabras especificadas,
#   en al menos uno de los campos especificados.
#
#6. limit=15: es la cantidad de registros que se recuperaran en la vista de autocompletar,
#   debe ser un valor entero positivo. este parametro es opcional. es la cantidad de
#   elementos que se veran en el autocompletar.
#
#7. to_field_name='pk': es el campo sobre el que se van a asociar los elementos enviados en
#   la request al momento de enviar los datos. es decir que cuando validemos se van a rescatar
#   los elementos que tengan un valor en dicho campo que sea igual al enviado (en caso de
#   referencia simple) o bien un valor entre los enviados (en caso de referencia multiple).
#   el campo pk existe en todas las tablas.
#
#8. throw403_if=None: es un predicado que toma un argumento: la peticion http actual. este
#   predicado corre cuando se conecta a una de las 3 urls registradas en este metodo. si
#   ante esa peticion http el predicado devuelve True, el resultado de la peticion pasa a
#   ser un error tipo 403. si no se especifica o es None, no ocurre nunca un error 403.
#
#9. throw404_if=None: es similar al anterior, pero el error generado es un 404.
#
#10.extra_data_getter=None: procesa el elemento actual para obtener algunos datos adicionales
#   que puedan ser usados en el front-end. si no se especifica entonces lo que llega como
#   'extra' en cada elemento es un objeto json vacio.

urlpatterns = patterns('',)\
  + lookups.registered_lookups['test_app.languages'].urls\
  + lookups.registered_lookups['test_app.speakers'].urls\
  + lookups.registered_lookups['test_app.groups'].urls