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
			{ 'pattern': r'^game/?$', 'method': 'view', 'right': 'connected' },
			{ 'pattern': r'^game/dungeon/([1-9][0-9]*)$', 'method': 'dungeon', 'right': 'connected' },
			{ 'pattern': r'^game/actions/([0-9]+,[0-9]+|r[0-9]+|0)/([0-9]+,[0-9]+|0)/([0-9]+)$', 'method': 'getactions', 'right': 'connected' }
		]
	
	def view(self, request):
		return self.templates.underConstruction()

	def chatrecv(self, request):
		return self.templates.underConstruction()

	def chatsend(self, request):
		return self.templates.underConstruction()

	def dungeon(self, request, gameid):
		return self.templates.response('game.dungeon', context={});

	def getactions(self, request, possrc, posdst, spawnid):
		return self.templates.response('game.getactions', context={});

	def action(self, request):
		return self.templates.underConstruction()

	def refresh(self, request):
		return self.templates.underConstruction()
