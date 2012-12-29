# *-* coding: utf-8 *-*
from django.core.urlresolvers import reverse
from django.template.context import RequestContext

__author__ = 'luismasuelli'
from models import SpeakerForm, Speaker
from django import http
from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf

def sample_form(request):
    if request.method == 'POST':
        sf = SpeakerForm(request.POST)
        if sf.is_valid():
            speaker = sf.save()
            return http.HttpResponseRedirect(reverse("sampleformok", args=[speaker.pk]))
        else:
            return render_to_response('test/form.html', {'form': sf}, context_instance=RequestContext(request))
    elif request.method == 'GET':
        return render_to_response('test/form.html', {'form': SpeakerForm()}, context_instance=RequestContext(request))
    else:
        return http.HttpResponseNotAllowed(['GET', 'POST'])


def sample_form_ok(request, speaker_id):
    speaker = get_object_or_404(Speaker, pk=speaker_id)
    return render_to_response('test/ok.html', {"speaker": speaker})