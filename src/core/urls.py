# -*- coding: utf-8 -*-
#
# This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
#

from django.conf.urls.defaults import patterns, url as urlsfunc
import settings
import core.controllers
import logging

LOGGER  = logging.getLogger('app')

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',)

for obj_name, obj in core.controllers.ApplicationContext.objects.iteritems():
	print obj
	if isinstance(obj, core.controllers.CommonController):
		LOGGER.debug('Load URLs for %s' % (str(obj_name)))
		for url in obj._geturls():
			name = url['name'] if 'name' in url.keys() else None
			prefix = url['prefix'] if 'prefix' in url.keys() else ''
			parameters = {
				'controller': obj_name,
				'method': url['method'],
				'right': url['right'] if 'right' in url.keys() else None
			}
			if 'parameters' in url.keys():
				for paramname in url['parameters'].keys():
					parameters[paramname] = url['parameters'][paramname]
			urlpatterns += patterns('', urlsfunc(url['pattern'], core.controllers.run_controller, parameters, name, prefix))
			LOGGER.info('%s => %s/%s for %s' % (url['pattern'], parameters['controller'], parameters['method'], parameters['right'] if parameters['right'] is not None else 'ALL'))

if settings.DEBUG:
	urlpatterns += patterns('', (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}))

