__author__ = 'Usuario'
from core import searched_queryset, initial_fk, initial_m2m, json_instance, json_list
from django.utils import simplejson
from django.http import HttpResponseNotFound, HttpResponseForbidden, HttpResponse
from django.views.decorators.csrf import csrf_exempt

def _autocomplete_error(request, throw403_if=None, throw404_if=None, context=''):
    if not (throw403_if is None) and throw403_if(request, context):
        return HttpResponseForbidden()
    if not (throw404_if is None) and throw404_if(request, context):
        return HttpResponseNotFound()
    return None

def _json_response(json_data):
    return HttpResponse(simplejson.dumps(json_data), content_type='application/javascript')

def _req_val(request, var):
    if request.method == 'POST':
        return request.POST[var] if var in request.POST else ''
    if request.method == 'GET':
        return request.GET[var] if var in request.GET else ''
    return ''

def autocomplete_search(request, queryset, filter, field_list, limit=15, to_field_name='pk', throw403_if=None, throw404_if=None, extra_data_getter=None):
    error = _autocomplete_error(request, throw403_if, throw404_if, 'ac')
    if error is not None:
        return error
    terms = _req_val(request, 'term')
    search_queryset = searched_queryset(queryset, filter, request, field_list, terms)
    return _json_response(json_list(search_queryset[:limit], to_field_name, extra_data_getter))

def autocomplete_fk_initial(request, queryset, filter, to_field_name='pk', throw403_if=None, throw404_if=None, extra_data_getter=None):
    error = _autocomplete_error(request, throw403_if, throw404_if, 'fk')
    if error is not None:
        return error
    try:
        value = simplejson.loads(_req_val(request, 'value'))
        element = initial_fk(queryset, filter, request, to_field_name, value)
        return _json_response(json_instance(element, to_field_name, extra_data_getter))
    except simplejson.JSONDecodeError as e:
        return _json_response(None)

@csrf_exempt
def autocomplete_m2m_initials(request, queryset, filter, to_field_name='pk', throw403_if=None, throw404_if=None, extra_data_getter=None):
    error = _autocomplete_error(request, throw403_if, throw404_if, 'm2m')
    if error is not None:
        return error
    try:
        values = simplejson.loads(_req_val(request, 'values'))
        elements = initial_m2m(queryset, filter, request, to_field_name, values)
        return _json_response(json_list(elements, to_field_name, extra_data_getter))
    except simplejson.JSONDecodeError as e:
        return _json_response([])