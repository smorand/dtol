# -*- coding: utf-8 -*-
#
# This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
#

from core.controllers import CommonController

class TournamentController(CommonController):
	'''
	Manage tournament
	'''
	
	def _geturls(self):
		return [
			{ 'pattern': r'^tournaments$', 'method': 'list', 'right': 'connected' },
		]

	def list(self, request):
		return self.templates.underConstruction()

	def create(self, request):
		return self.templates.underConstruction()

	def subscribe(self, request):
		return self.templates.underConstruction()

	def forfeit(self, request):
		return self.templates.underConstruction()

	def delete(self, request):
		return self.templates.underConstruction()
