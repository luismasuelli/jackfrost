# encoding: latin-1
import json as simplejson

__author__ = 'Usuario'

from lookups import registered_lookups
from core import AutocompleteError
from django.forms.fields import Field, CharField
from django.forms.models import ModelMultipleChoiceField
from django.forms import Media
from widgets import AutocompleteTextInput, AutocompleteSelect, AutocompleteSelectMultiple
from django.forms import ValidationError
from django.db.models import Model
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from threading import local


class AutocompleteFieldError(AutocompleteError):
    pass


class AutocompleteField(object):
    """
    Autocomplete field:
      Allows access to lookups and so.
      It also has threadlocals specifying a request for the field so it can perform
      custom validation. That validation is performed against a filtered
      queryset: a (mandatory) model to filter and a (non-mandatory) callable
      taking two arguments: the queryset to filter (with a starting value of
      MODEL.objects.all()) and the current request. That callable can perform
      custom filters like retrieving the current session user and allowing to
      get only model objects related to that user, and many additional examples.
    """

    DATA = local()

    def __init__(self, lookup_name):
        """
        Sets the current lookup name. It does not yet evaluate the validity.
        Validity is lazy-evaluated.
        """
        self._lookup_name = lookup_name

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

    @staticmethod
    def set_request(request):
        AutocompleteField.DATA.request = request

    @staticmethod
    def unset_request(request):
        AutocompleteField.DATA.request = None

    @staticmethod
    def get_request():
        try:
            return AutocompleteField.DATA.request
        except AttributeError as e:
            return None


class AutocompleteCharField(AutocompleteField, CharField):
    def __init__(self, lookup_name, *args, **kwargs):
        kwargs.pop('widget', 1) #dummy True value, to remove widget argument
        CharField.__init__(self, widget=AutocompleteTextInput(lookup_name, kwargs.pop('widget_attrs')), *args, **kwargs) #setting current widget as  an autocomplete text input
        AutocompleteField.__init__(self, lookup_name)


class AutocompleteModelChoiceField(AutocompleteField, Field):
    """
    Model choice field with autocomplete facilities.
    """

    default_error_messages = {
        'invalid_choice': _(u'Select a valid choice. That choice is not one of'
                            u' the available choices.'),
    }

    def __init__(self, lookup_name, *args, **kwargs):
        kwargs.pop('widget', 1) #dummy True value, to remove widget argument
        Field.__init__(self, widget=AutocompleteSelect(lookup_name, kwargs.pop('widget_attrs')), *args, **kwargs) #setting current widget as  an autocomplete text input
        AutocompleteField.__init__(self, lookup_name)

    def to_python(self, value):
        lookup = self._get_lookup()
        errors = self.error_messages

        if isinstance(value, Model):
            value = value.serializable_value(lookup.to_field_name)
        elif value is None:
            return None

        return lookup.clean_fk(value, AutocompleteField.get_request(), errors)

    def clean(self, value):
        if self.required and not value:
            raise ValidationError(self.error_messages['required'])

        cleaned_value = self.to_python(value)

        self.run_validators(cleaned_value)

        return cleaned_value

    def prepare_value(self, value):
        return simplejson.dumps(value)


class AutocompleteModelMultipleChoiceField(AutocompleteField, Field):
    """
    Multiple model choice field with autocomplete facilities. does a post to retrieve
    data using a large amount of identifiers.
    """

    default_error_messages = {
        'invalid_choice': _(u'Select a valid choice. That choice is not one of'
                            u' the available choices.'),
        'list': _(u'The supplied value should be a list or tuple.')
    }

    def __init__(self, lookup_name, *args, **kwargs):
        kwargs.pop('widget', 1) #dummy True value, to remove widget argument
        Field.__init__(self, widget=AutocompleteSelectMultiple(lookup_name, kwargs.pop('widget_attrs')), *args, **kwargs)
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

        return lookup.clean_m2m((self._single_value_to_python(v) for v in values), AutocompleteField.get_request(), errors)

    def clean(self, values):
        if self.required and not values:
            raise ValidationError(self.error_messages['required'])

        cleaned_values = self.to_python(values)

        self.run_validators(cleaned_values)

        return cleaned_values

    def prepare_value(self, values):
        return simplejson.dumps(values)
