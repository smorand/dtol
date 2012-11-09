# -*- coding: utf-8 -*-
#
# This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
#

from core.controllers import CommonController

class StatisticsController(CommonController):
	'''
	Manage and display statistics
	'''
	
	def _geturls(self):
		return [
			{ 'pattern': r'^statistics$', 'method': 'classment', 'right': 'connected' },
		]
	
	def classment(self, request):
		return self.templates.underConstruction()

	def classmentplayer(self, request):
		return self.templates.underConstruction()

	def create(self, request):
		return self.templates.underConstruction()
		
