# -*- coding: utf-8 -*-
#
# This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
#

from core.controllers import CommonController

class TeamController(CommonController):
	'''
	Manage team
	'''
	
	def _geturls(self):
		return [
			{ 'pattern': r'^teams$', 'method': 'list' },
		]

	def list(self, request):
		return self.templates.response('team_list', context={ 'teams': self.teamManager.getTeams(user=request.session['user']) })
	
	def create(self, request):
		user = request.session['user']
		return self.templates.response('team_create', context={
			'characters': self.spawnManager.getCharacters(user.extensions),
			'objects': self.spawnManager.getObjects(self.user.extensions),
			'rooms': self.spawnManager.getRooms(user.extensions)
		})
	
	def update(self, request):
		return self.templates.underConstruction()
	
	def delete(self, request):
		return self.templates.underConstruction()
	
	def randomCreate(self, request):
		return self.templates.underConstruction()
	
	
