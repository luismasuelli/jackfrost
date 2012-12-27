# encoding: latin-1
__author__ = 'Usuario'

from lookups import registered_lookups
from core import AutocompleteError
from django.forms.fields import Field, CharField
from django.forms.models import ModelMultipleChoiceField
from widgets import AutocompleteTextInput, AutocompleteSelect, AutocompleteSelectMultiple
from django.forms import ValidationError
from django.db.models import Model
from django.utils.translation import ugettext_lazy as _

class AutocompleteFieldError(AutocompleteError):
    pass


class AutocompleteField(object):
    """
    Autocomplete field:
      Allows access to lookups and so.
      It also allows specifying a request for the field so it can perform
      custom validation. That validation is performed against a filtered
      queryset: a (mandatory) model to filter and a (non-mandatory) callable
      taking two arguments: the queryset to filter (with a starting value of
      MODEL.objects.all()) and the current request. That callable can perform
      custom filters like retrieving the current session user and allowing to
      get only model objects related to that user, and many additional examples.
    """

    def __init__(self, lookup_name):
        """
        Sets the current lookup name. It does not yet evaluate the validity.
        Validity is lazy-evaluated.
        """
        self._lookup_name = lookup_name
        self._request = None

    def _get_lookup(self):
        """
        Gets the custom lookup. This is useful only for clean purposes.
        Initial values are set as integer elements, and labels are
        retrieved via ajax.
        """
        try:
            global registered_lookups
            return registered_lookups[self._lookup_name]
        except Exception as e:
            return AutocompleteFieldError("Unregistered '%s' autocomplete lookup" % self._lookup_name)

    def _set_request(self, request):
        """
        Called by set_request_in_each_field to set the current request
        in this field.
        """
        self._request = request

    @staticmethod
    def set_request_in_each_field(form, request):
        """
        This method runs each form field, affecting only AutocompleteFields.
        Sets the current request. This is useful only for clean purposes.
        This method must be called before any clean operation takes place.
        A good point where to call this method may be after the form
        creation. Note: this is a static method.
        """
        for field in form.fields:
            if isinstance(field, (AutocompleteField,)):
                field._set_request(request)


#no es otra cosa que un CharField ...
#lo unico diferente es el widget.
#
#ni nos molestamos en validar, en este, si el lookup es bueno.
#de esa validacion se encargará el widget.
class AutocompleteCharField(AutocompleteField, CharField):
    def __init__(self, lookup_name, *args, **kwargs):
        kwargs.pop('widget', 1) #dummy True value, to remove widget argument
        CharField.__init__(self, widget=AutocompleteTextInput(lookup_name), *args, **kwargs) #setting current widget as  an autocomplete text input
        AutocompleteField.__init__(self, lookup_name)


class AutocompleteModelChoiceField(AutocompleteField, Field):
    default_error_messages = {
        'invalid_choice': _(u'Select a valid choice. That choice is not one of'
                            u' the available choices.'),
    }

    #additional widget_attrs are:
    #  before_del, after_del, before_set, after_set : events
    def __init__(self, lookup_name, *args, **kwargs):
        kwargs.pop('widget', 1) #dummy True value, to remove widget argument
        Field.__init__(self, widget=AutocompleteSelect(lookup_name, kwargs.get('widget_attrs')), *args, **kwargs) #setting current widget as  an autocomplete text input
        AutocompleteField.__init__(self, lookup_name)

    def to_python(self, value):
        lookup = self._get_lookup()
        errors = self.error_messages

        if isinstance(value, Model):
            value = value.serializable_value(lookup.to_field_name)
        elif value is None:
            return None

        return lookup.clean_fk(value, self._request, errors)

    def clean(self, value):
        if self.required and not value:
            raise ValidationError(self.error_messages['required'])

        cleaned_value = self.to_python(value)

        self.run_validators(cleaned_value)

        return cleaned_value


class AutocompleteModelMultipleChoiceField(AutocompleteField, Field):
    default_error_messages = {
        'invalid_choice': _(u'Select a valid choice. That choice is not one of'
                            u' the available choices.'),
        'list': _(u'The supplied value should be a list or tuple.')
    }

    #additional widget_attrs are:
    #  before_rem, after_rem, before_add, after_add : events
    def __init__(self, lookup_name, *args, **kwargs):
        kwargs.pop('widget', 1) #dummy True value, to remove widget argument
        Field.__init__(self, widget=AutocompleteSelectMultiple(lookup_name, kwargs.get('widget_attrs')), *args, **kwargs)
        AutocompleteField.__init__(self, lookup_name)

    def _single_value_to_python(self, value):
        if isinstance(value, Model):
            value = value.serializable_value(self._get_lookup().to_field_name)
        elif value is None:
            return None
        return value

    def to_python(self, values):
        lookup = self._get_lookup()
        errors = self.error_messages

        if not values:
            values = []
        if not isinstance(values, (list, tuple)):
            raise ValidationError(self.error_messages['list'])

        return lookup.clean_m2m([self._single_value_to_python(v) for v in values], self._request, errors)

    def clean(self, values):
        if self.required and not values:
            raise ValidationError(self.error_messages['required'])

        cleaned_values = self.to_python(values)

        self.run_validators(cleaned_values)

        return cleaned_values
