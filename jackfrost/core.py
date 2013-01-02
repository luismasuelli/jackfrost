__author__ = 'Usuario'
from django.db.models import Q, Model, ObjectDoesNotExist
from django.utils.encoding import force_unicode

import re

def query_filter(request, query, filter):
    return query if filter is None else filter(query, request)

def searched_queryset(queryset, filter, request, field_list, terms=''):
    term_list = [x for x in re.split(r'\s+', terms) if x != '']
    look_list = [x+'__icontains' for x in field_list]
    search_filter = Q()
    for term in term_list:
        search_filter_for_term = Q()
        for look in look_list:
            search_filter_for_term |= Q(**{look: term})
        search_filter &= search_filter_for_term
    return query_filter(request, queryset, filter).filter(search_filter)

def initial_fk(queryset, filter, request, to_field, value):
    if value is None:
        return None
    try:
        return query_filter(request, queryset, filter).get(**{to_field: value})
    except ObjectDoesNotExist:
        return None

def initial_m2m(queryset, filter, request, to_field, values):
    if values is None:
        return []
    return query_filter(request, queryset, filter).filter(**{to_field + '__in': values})

def json_instance(instance, to_field, extra_data_getter=None):
    return {
        'key': instance.serializable_value(to_field),
        'label': force_unicode(instance),
        'extra': {} if extra_data_getter is None else extra_data_getter(instance)
    }

def json_list(instances, to_field, extra_data_getter=None):
    return [json_instance(x, to_field, extra_data_getter) for x in instances]

class AutocompleteError(Exception):
    pass