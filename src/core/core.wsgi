# coding: utf8

import os
import sys
__realpath = os.path.dirname(os.path.realpath(__file__))
if __realpath not in sys.path:
	sys.path.insert(0, __realpath)
import settings

sys.path.insert(0, settings.APPLICATION_ROOT)
if type(settings.EXTERNAL_PATH) == list:
	sys.path.extend(settings.EXTERNAL_PATH)
if type(settings.EXTERNAL_PATH_BEFORE) == list:
	for p in EXTERNAL_PATH_BEFORE: sys.path.insert(1, p)
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

