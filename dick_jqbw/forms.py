__author__ = 'Usuario'
from django.forms import Media
from django.forms import Form
from django.forms.models import ModelForm
from widgets import JQueryWidget

class JQueryFormTrait(object):
    JQUERY_VERSION = "1.6.2"
    JQUERY_UI_VERSION = "1.8.16"
    JQUERY_UI_THEME = "base"

    @staticmethod
    def _create_media(jqversion, jquiversion, jquitheme):
        css = (
            'css/themes/base/jquery-ui.css' if jquitheme == 'base' else 'css/themes/%s/jquery-ui-%s.custom.css' % (jquitheme, jquiversion),
        )
        jquiscript = 'js/jquery-ui-%s.custom.min.js' % jquiversion
        jqscript = 'js/jquery-%s.min.js' % jqversion
        return Media(css={'all': css}, js=(jqscript, jquiscript))

    def set_media(self, jqversion=JQUERY_VERSION, jquiversion=JQUERY_UI_VERSION, jquitheme=JQUERY_UI_THEME):
        self._jqui_media = JQueryFormTrait._create_media(jqversion, jquiversion, jquitheme)

    def jquery_enhaced_media(self):
        if hasattr(self, 'media'):
            return getattr(self, 'media') + self._jqui_media
        else:
            return self._jqui_media

    def __init__(self):
        self.set_media()

class JQueryModelForm(ModelForm, JQueryFormTrait):
    def __init__(self, *args, **kwargs):
        ModelForm.__init__(self, *args, **kwargs)
        JQueryFormTrait.__init__(self)

class JQueryForm(Form, JQueryFormTrait):
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        JQueryFormTrait.__init__(self)