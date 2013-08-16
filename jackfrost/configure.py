# *-* coding: utf-8 *-*
from django.conf import settings

"""
This file is used to configure the environment for variables regarding static files and styles.
This file is called inside of the package initializer.

These variables must be set to file locations relative to the static directory, and populating the
staticfiles should be done by hand.

JACKFROST_JQUERY_LIB : the jquery script to use in the website.
JACKFROST_JQUERYUI_LIB : jquery-ui is needed to run this app. the jquery-ui script must be placed here.
JACKFROST_JQUERY_CSS : the css needed for the jquery-ui library.

If no values are provided, default  files and themes are used. These defaults are shipped within the
JACKFROST application.
"""

if not settings.configured:
    settings.configure(JACKFROST_INSTALLED=True)
else:
    settings.JACKFROST_INSTALLED=True
if not getattr(settings, 'JACKFROST_JQUERY_LIB', None):
    settings.JACKFROST_JQUERY_LIB = 'js/jquery-1.6.2.min.js'
if not getattr(settings, 'JACKFROST_JQUERYUI_LIB', None):
    settings.JACKFROST_JQUERYUI_LIB = 'js/jquery-ui-1.8.16.custom.min.js'
if not getattr(settings, 'JACKFROST_JQUERYUI_CSS', None):
    settings.JACKFROST_JQUERYUI_CSS = 'css/themes/base/jquery-ui.css'
if not 'jackfrost.middlewares.AutocompleteMiddleware' in settings.MIDDLEWARE_CLASSES:
    settings.MIDDLEWARE_CLASSES = settings.MIDDLEWARE_CLASSES + ('jackfrost.middlewares.AutocompleteMiddleware',)