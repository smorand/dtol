# -*- coding: utf-8 -*-
#
# This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
#

from django.http import HttpResponse
from django.template import Context
from django.utils.translation import ugettext as _
import controllers

class AuthenticationController(controllers.CommonController):
	'''
	classdocs
	'''

	def _geturls(self):
		return [
			{ 'pattern': r'^auth//([a-z]+)$', 'method': 'setlang' }
		]
	
	def authenticate(self, request, lang):
		t = self.templates.message_return
		response = HttpResponse()
		response.set_cookie('lang', lang)
		response.write(t.render(Context({})))
		return response

