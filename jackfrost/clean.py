__author__ = 'Usuario'
from django.db.models import ObjectDoesNotExist
from django.forms import ValidationError
from django.utils.translation import ugettext as _
from core import query_filter

def validate_fk(queryset, request, filter, value, to_field, error_messages):
    try:
        return query_filter(request, queryset, filter).get(**{to_field: value})
    except ObjectDoesNotExist:
        message = error_messages['invalid'] if 'invalid' in error_messages else _(u'Select a valid choice. %s is not one of the available choices.') % value
        x = ValidationError(message)
        x.code = 'invalid_choice'
        raise x
    except ValueError:
        message = error_messages['invalid_pk_value'] % value
        x = ValidationError(message)
        x.code = 'invalid_pk_value'
        raise x
    except Exception as e:
        message = e.message
        x = ValidationError(message)
        x.code = 'other'
        raise x

def validate_m2m(queryset, request, filter, values, to_field, error_messages):
    v = 0
    try:
        t = query_filter(request, queryset, filter)
        for v in values:
            t.get(**{to_field: v})
        return t
    except ObjectDoesNotExist:
        message = error_messages['invalid_choice'] if 'invalid_choice' in error_messages else _(u'Select a valid choice. %s is not one of the available choices.') % v
        x = ValidationError(message)
        x.code = 'invalid_choice'
        raise x
    except ValueError:
        message = error_messages['invalid_pk_value'] % v
        x = ValidationError(message)
        x.code = 'invalid_pk_value'
        raise x
    except Exception as e:
        message = e.message
        x = ValidationError(message)
        x.code = 'other'
        raise x


  