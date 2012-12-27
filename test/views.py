# *-* coding: utf-8 *-*
__author__ = 'luismasuelli'
from models import SpeakerForm, Speaker
from django import http
from django.shortcuts import render_to_response

def sample_form(request):
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        pass
    else:
        return http.HttpResponseNotAllowed(['GET', 'POST'])


def sample_form_ok(request, speaker):
    speaker = Speaker.objects.get
    render_to_response('ok.html')