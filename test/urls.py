#coding: utf-8
from django.conf.urls import patterns, include, url
from jackfrost import lookups
from models import Speaker, Group, Language
from views import *

#test function to use as filter criteria. it does not distinguish (YET)
#the context in which it is called (autocomplete, initial FK, initial M2M)
def spamfinder(request, context):
    term = request.GET.get('term', '')
    terms = term.lower().split()
    return "spam" in terms

def eggsfinder(request, context):
    term = request.GET.get('term', '')
    terms = term.lower().split()
    return "eggs" in terms

def test_filter(query, request):
    print "filtrando la request " + str(request)
    return query

lookups.register(
    r'^speakers-%s/$',
    'test_app.speakers',
    Speaker.objects.all(),
    test_filter,
    ('name',),
    throw403_if=spamfinder,
    throw404_if=eggsfinder
)

lookups.register(
    r'^languages-%s/$',
    'test_app.languages',
    Language.objects.all(),
    test_filter,
    ('name',),
    throw403_if=spamfinder,
    throw404_if=eggsfinder
)

lookups.register(
    r'^groups-%s/$',
    'test_app.groups',
    Group.objects.all(),
    test_filter,
    ('description',),
    throw403_if=spamfinder,
    throw404_if=eggsfinder
)

urlpatterns = patterns('',
    url(r'^send/', sample_form, name="sampleform"),
    url(r'^ok/(\d+)/', sample_form_ok, name="sampleformok"),
  )\
  + lookups.registered_lookups['test_app.languages'].urls\
  + lookups.registered_lookups['test_app.speakers'].urls\
  + lookups.registered_lookups['test_app.groups'].urls