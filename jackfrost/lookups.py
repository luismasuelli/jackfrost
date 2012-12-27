from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse

from clean import validate_fk, validate_m2m

registered_lookups = {}

class JQACLookup(object):
    def __init__(self, name, urls, clean_fk, clean_m2m, to_field_name):
        self.name = name
        self.urls = urls
        self.clean_fk = clean_fk
        self.clean_m2m = clean_m2m
        self.to_field_name = to_field_name
    def reverse_autocomplete_url(self):
        return reverse(self.name + '-ac')
    def reverse_fk_initial_url(self):
        return reverse(self.name + '-one')
    def reverse_m2m_initials_url(self):
        return reverse(self.name + '-many')

def register(pattern, name, queryset, filter, field_list, limit=15, to_field_name='pk', throw403_if=None, throw404_if=None, extra_data_getter=None):
    if name in registered_lookups:
        return
    lookup_urls = patterns('',
        url(pattern % ('ac',), 'dick_jqac_json.views.autocomplete_search', name=name+'-ac', kwargs={'field_list': field_list, 'queryset' : queryset, 'limit':limit, 'filter': filter, 'to_field_name': to_field_name, 'throw403_if': throw403_if, 'throw404_if': throw404_if, 'extra_data_getter': extra_data_getter }),
        url(pattern % ('many',), 'dick_jqac_json.views.autocomplete_m2m_initials', name=name+'-many', kwargs={'queryset' : queryset, 'filter': filter, 'to_field_name': to_field_name, 'throw403_if': throw403_if, 'throw404_if': throw404_if, 'extra_data_getter': extra_data_getter }),
        url(pattern % ('one',), 'dick_jqac_json.views.autocomplete_fk_initial', name=name+'-one', kwargs={'queryset' : queryset, 'filter': filter, 'to_field_name': to_field_name, 'throw403_if': throw403_if, 'throw404_if': throw404_if, 'extra_data_getter': extra_data_getter }),
    )
    lookup_validate_fk = lambda value, request, error_dict: validate_fk(queryset, request, filter, value, to_field_name, error_dict)
    lookup_validate_m2m = lambda values, request, error_dict: validate_m2m(queryset, request, filter, values, to_field_name, error_dict)
    lu = JQACLookup(name, lookup_urls, lookup_validate_fk, lookup_validate_m2m, to_field_name)
    registered_lookups[name] = lu