# -*- coding: utf-8 -*-
#
# This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
#

'''
List of controllers, with indirections to object loaded by Spring
'''

import springpython.context
from django.http import HttpResponse
from django.template import loader, Context
from os import listdir
from os.path import isdir, isfile, sep
from settings import APPLICATION_CONTEXTS, TEMPLATE_DIRS, DEBUG
import logging

LOGGER = logging.getLogger('app')

class CommonController(object):
	
	def __init__(self):
		self.prehandler = None
		self.posthandler = None
		self.urls = []

	def _geturls(self):
		raise Exception("No URL defined")

	def prehandle(self, request):
		tpl = None
		if isinstance(self.prehandler, list):
			for ph in self.prehandler:
				if isinstance(ph, PreHandler):
					tpl = ph.handle(request)
				if tpl != None:
					break
		elif isinstance(self.prehandler, PreHandler):
			tpl = self.prehandler.handle(request)
		return tpl

	def posthandle(self, request, tpl):
		if isinstance(self.posthandler, list):
			for ph in self.posthandler:
				if isinstance(ph, PostHandler):
					ph.handle(request, tpl)
		elif isinstance(self.posthandler, PostHandler):
			self.posthandler.handle(request, tpl)

class PreHandler(object):

	def handle(self, request):
		pass

class PostHandler(object):

	def handle(self, request, tpl):
		pass

# Templates loading
class TemplatesContainer(object):
	
	def __init__(self, tpldir=TEMPLATE_DIRS, prefix=''):
		self.__templates = {}
		self.__tpldir = tpldir
		self.__prefix = prefix
		self.__load()
	
	def after_properties_set(self):
		pass
	
	def set_app_context(self, context):
		pass
	
	def __load(self):
		# Load all templates found. Replace directory by _
		for fileent in listdir(self.__tpldir):
			if isfile(self.__tpldir + sep + fileent):
				self.__templates[fileent.replace('.html', '')] = loader.get_template(self.__prefix + fileent)
			elif isdir(self.__tpldir + sep + fileent):
				self.__templates[fileent] = TemplatesContainer(self.__tpldir + sep + fileent, self.__prefix + fileent + sep)
	
	def __getattr__(self, name):
		if DEBUG:
			self.__load()
		if name not in self.__templates:
			LOGGER.error('Internal error: Template %s is missing' % (name))
			raise Exception('Internal error: Template %s is missing' % (name))
		return self.__templates[name]
	
	def render(self, name, context={}):
		name_i = name.split('.', 2)
		tpl = self
		while type(tpl) == TemplatesContainer:
			try:
				tpl = tpl.__getattr__(name_i.pop(0))
			except:
				LOGGER.error('Internal error: Template %s is missing' % (name))
				raise Exception('Internal error: Template %s is missing' % (name))
		return tpl.render(Context(context))
			
	def content(self, content):
		return HttpResponse(content=content, mimetype="text/html", status=200)
			
	def response(self, name, context={}, status=200, mimetype="text/html"):
		return HttpResponse(content=self.render(name, context), mimetype=mimetype, status=status)
	
	def redirect(self, url):
		return HttpResponse(content='<html><head><meta http-equiv="refresh" content="0; url=%s"/></head></html>' % url, mimetype="text/html", status=200)
	
	def forbidden(self):
		return self.response('forbidden')
	
	def empty(self):
		return self.content('')
			
	def error(self, msg):
		return self.response('message_return', { 'error':msg })
			
	def underConstruction(self):
		return self.response('under_construction')
		
# Controllers are entry point of the application, so this is the good place to load the application (lazy loading)
ApplicationContext = springpython.context.ApplicationContext(APPLICATION_CONTEXTS)

'''
Declare controller. This first layer has two purposes :
1/ Check security
2/ Call the IoC managed controller method
'''
	
# Controllers
templates = ApplicationContext.get_object('templatesContainer')

controllersmap = {}

def run_controller(request, *kargs, **kwargs):
	kwargsremain = {}
	for key, val in kwargs.iteritems():
		if key == 'controller':
			controller = kwargs['controller']
		elif key == 'method':
			method = kwargs['method']
		elif key == 'right':
			right = kwargs['right']
		else:
			kwargsremain[key] = val
	if controller not in controllersmap.keys():
		controllersmap[controller] = ApplicationContext.get_object(controller)
	controllerObj = controllersmap[controller]
	try:
		if right is not None and request.session.get(right, default=None) is None:
			tpl = templates.forbidden()
		else:
			tpl = controllerObj.prehandle(request)
			if tpl is None:
				tpl = getattr(controllerObj, method)(request, *kargs, **kwargsremain)
				controllerObj.posthandle(request, tpl)
	except Exception as exc:
		tpl = templates.error(exc)
	return tpl

