# -*- coding: utf-8 -*-
#
# This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
#

from core.controllers import CommonController

class GameController(CommonController):
	'''
	Game controller, main entry point to the engine of the game
	'''
	
	def _geturls(self):
		return [
			{ 'pattern': r'^/game?$', 'method': 'view' },
		]
	
	def view(self, request):
		return self.templates.underConstruction()

	def chatrecv(self, request):
		return self.templates.underConstruction()

	def chatsend(self, request):
		return self.templates.underConstruction()

	def getactions(self, request):
		return self.templates.underConstruction()

	def action(self, request):
		return self.templates.underConstruction()

	def refresh(self, request):
		return self.templates.underConstruction()
