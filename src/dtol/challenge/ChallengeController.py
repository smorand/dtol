# -*- coding: utf-8 -*-
#
# This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
#

from core.controllers import CommonController

class ChallengeController(CommonController):
	'''
	Entry point linked to defis
	'''
	
	def _geturls(self):
		return [
			{ 'pattern': r'^challenges$', 'method': 'list' },
		]

	def list(self, request):
		return self.templates.underConstruction()
		
	def create(self, request):
		return self.templates.underConstruction()
		
	def cancel(self, request):
		return self.templates.underConstruction()
		
	def unCancel(self, request):
		return self.templates.underConstruction()
		
	def accept(self, request):
		return self.templates.underConstruction()
		
	def setTeam(self, request):
		return self.templates.underConstruction()
		
