from django.conf import settings

__author__ = 'Usuario'

from lookups import registered_lookups
from core import AutocompleteError
from django.forms.widgets import TextInput, SelectMultiple, Input
from django.utils.safestring import mark_safe
from django.forms import Media
from django.utils.encoding import force_unicode
from django.forms.util import flatatt
from django.forms.widgets import Widget
import json as simplejson
import uuid


class AutocompleteWidgetError(AutocompleteError):
    pass


class AutocompleteWidget(Widget):

    @property
    def media(self):
        jcss = settings.JACKFROST_JQUERYUI_CSS
        jjql = settings.JACKFROST_JQUERY_LIB
        jjqu = settings.JACKFROST_JQUERYUI_LIB
        return Media(
            css={'all': (jcss,)},
            js=(jjql, jjqu, 'js/JSON.js', 'js/jackfrost.js'
        ))

    def __init__(self, lookup_name, attrs=None):
        super(AutocompleteWidget, self).__init__(attrs)
        self._lookup_name = lookup_name

    def _must_have_id(self, attrs=None):
        uniqid = uuid.uuid4()
        if isinstance(attrs, dict):
            if not attrs.has_key('id'):
                attrs['id'] = u'jackfrost_id_' + uniqid
            return attrs
        else:
            return dict(id=u'jackfrost_id_' + uniqid)

    def _get_lookup(self):
        try:
            global registered_lookups
            return registered_lookups[self._lookup_name]
        except Exception as e:
            raise AutocompleteWidgetError("Unregistered '%s' autocomplete lookup" % self._lookup_name)


class AutocompleteTextInput(AutocompleteWidget, TextInput):
    """
    Simple text-box with jquery AC enabled features.
    """

    def __init__(self, lookup_name, attrs=None):
        TextInput.__init__(self, attrs)
        AutocompleteWidget.__init__(self, lookup_name, attrs)

    def render(self, name, value, attrs=None):
        attrs = self._must_have_id(attrs)
        return TextInput.render(self, name, value, attrs) + self.render_jquery_autocomplete(attrs)

    def render_jquery_autocomplete(self, attrs):
        url = self._get_lookup().reverse_autocomplete_url()
        id = attrs['id']
        custom_renderer = attrs.get('renderer', 'undefined')
        autocomplete_textinput_template = u"""
        <script>
          (function($){
            $(function(){
              jackfrost_input($, %s, %s, %s);
            });
          })(jQuery);
        </script>
        """
        texto = autocomplete_textinput_template % (
            simplejson.dumps(id),
            simplejson.dumps(url),
            simplejson.dumps(custom_renderer)
        )
        return mark_safe(texto)


class AutocompleteSelect(AutocompleteWidget, Input):
    """
    Simple model choice field whose value comes from a source and validates against it.
    """

    def value_from_datadict(self, data, files, name):
        return simplejson.loads(data[name])

    def __init__(self, lookup_name, attrs=None):
        Input.__init__(self, attrs)
        AutocompleteWidget.__init__(self, lookup_name, attrs)

    def render(self, name, value, attrs=None):
        attrs = self._must_have_id(attrs)
        attrs.pop('name', 1)
        return self.render_controls(name, attrs) +\
               self.render_jquery_autocomplete(value, attrs)

    def render_controls(self, name, attrs=None):
        final_attrs = self.build_attrs(attrs)
        #esto para darle id al cuadro de texto y al hidden
        #el nombre no lo usamos ya que no queremos el textbox como elemento
        #del formulario a enviar.
        control_id = final_attrs['id']
        final_attrs['id'] += '-text'
        final_attrs['type'] = 'text'
        textbox = mark_safe(u'<input %s />' % flatatt(final_attrs))
        hidden  = mark_safe(u'<input id="%s" type="hidden" name="%s" />' % (control_id, name))
        return textbox + hidden

    def render_jquery_autocomplete(self, value, attrs):
        attrs = self.build_attrs(attrs)
        url_ac = self._get_lookup().reverse_autocomplete_url()
        url_init = self._get_lookup().reverse_fk_initial_url()
        id = attrs['id']
        before_set = attrs.get('before_set', 'undefined')
        after_set = attrs.get('after_set', 'undefined')
        before_del = attrs.get('before_del', 'undefined')
        after_del = attrs.get('after_del', 'undefined')
        custom_renderer = attrs.get('renderer', 'undefined')
        autocomplete_fk_template = u"""
        <script>
          (function($){
            $(function(){
              jackfrost_singlechoice($, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            });
          })(jQuery);
        </script>
        """
        return mark_safe(autocomplete_fk_template % (
            simplejson.dumps(id),
            simplejson.dumps(url_ac),
            simplejson.dumps(url_init),
            value,
            before_set,
            after_set,
            before_del,
            after_del,
            custom_renderer
        ))


class AutocompleteSelectMultiple(AutocompleteWidget, Input):
    """
    Multiple model choice field with a select multiple and a text enabled with jquery AC capabilities.
    Validates the list of values against a source.
    """

    def value_from_datadict(self, data, files, name):
        return simplejson.loads(u'[' + data[name][1 : -1] + u']')

    def __init__(self, lookup_name, attrs=None):
        Input.__init__(self, attrs)
        AutocompleteWidget.__init__(self, lookup_name, attrs)

    def render(self, name, value, attrs=None):
        attrs = self._must_have_id(attrs)
        attrs.pop('name', 1)
        return self.render_controls(name, attrs) +\
               self.render_jquery_autocomplete(value, attrs)

    def render_controls(self, name, attrs=None):
        final_attrs = self.build_attrs(attrs)
        #esto para darle id al cuadro de texto y al hidden
        #el nombre no lo usamos ya que no queremos el textbox como elemento
        #del formulario a enviar.
        control_id = final_attrs['id']
        final_attrs['id'] += '-text'
        final_attrs['type'] = 'text'
        textbox = mark_safe(u'<input %s />' % flatatt(final_attrs))
        hidden  = mark_safe(u'<input id="%s" type="hidden" name="%s" />' % (control_id, name))
        lista   = mark_safe(u'<select id="%s" multiple="multiple"></select>' % (control_id + '-list',))
        return textbox + hidden + u'<br/>' + lista

    def render_jquery_autocomplete(self, values, attrs):
        attrs = self.build_attrs(attrs)
        if values is None:
            values = []
        url_ac = self._get_lookup().reverse_autocomplete_url()
        url_init = self._get_lookup().reverse_m2m_initials_url()
        id = attrs['id']
        before_add = attrs.get('before_add', 'undefined')
        after_add = attrs.get('after_add', 'undefined')
        before_rem = attrs.get('before_rem', 'undefined')
        after_rem = attrs.get('after_rem', 'undefined')
        custom_renderer = attrs.get('renderer', 'undefined')
        autocomplete_m2m_template = u"""
        <script>
          (function($)
          {
            $(function(){
              jackfrost_multichoice($, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            });
          })
          (jQuery);
        </script>
        """
        return mark_safe(autocomplete_m2m_template % (
            simplejson.dumps(id),
            simplejson.dumps(url_ac),
            simplejson.dumps(url_init),
            values,
            before_add,
            after_add,
            before_rem,
            after_rem,
            custom_renderer
        ))