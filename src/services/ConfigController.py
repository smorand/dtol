# -*- coding: utf-8 -*-
#
# This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
#

from django.http import HttpResponse
from django.template import Context
from django.utils.translation import ugettext as _
from core.controllers import CommonController

class ConfigController(CommonController):
	'''
	classdocs
	'''

	def _geturls(self):
		return [
			{ 'pattern': r'^config/lang/([a-z]+)$', 'method': 'setlang' }
		]
	
	def setlang(self, request, lang):
		t = self.templates.message_return
		response = HttpResponse()
		response.set_cookie('lang', lang)
		response.write(t.render(Context({})))
		return response

