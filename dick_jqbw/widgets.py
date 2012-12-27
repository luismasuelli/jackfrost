__author__ = 'Usuario'
from django.forms.widgets import Widget
import uuid

class JQueryWidget(Widget):
    def _must_have_id(self, attrs=None):
        uniqid = uuid.uuid4()
        if isinstance(attrs, dict):
            if not attrs.has_key('id'):
                attrs['id'] = u'jqbasewidget_id_' + uniqid
            return attrs
        else:
            return dict(id=u'jqbasewidget_id_' + uniqid)