# *-* coding: utf-8 *-*
__author__ = 'luismasuelli'
from fields import AutocompleteField

class AutocompleteMiddleware(object):

    def process_request(self, request):
        AutocompleteField.set_request(request)

    def process_template_response(self, request, response):
        AutocompleteField.unset_request(request)
        return response

    def process_response(self, request, response):
        AutocompleteField.unset_request(request)
        return response

    def process_exception(self, request, exception):
        AutocompleteField.unset_request(request)
        return None