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
			{ 'pattern': r'^challenges$', 'method': 'list', 'right': 'connected' },
			{ 'pattern': r'^challenges/create$', 'method': 'create', 'right': 'connected' },
			{ 'pattern': r'^challenges/save$', 'method': 'create', 'right': 'connected' },
		]

	def list(self, request):
		c = {
			
		}
		return self.templates.response('challenge.list', context=c)
		
	def create(self, request):
		extensions = self.userManager.getUser(request.session['user'].id).extensions.all()
		c = {
			'users': self.userManager.getUsersExcept([request.session['user'].login]),
			'extensions': extensions,
			'constraints': self.teamManager.getTeamConstraints(),
		}
		return self.templates.response('challenge.edit', context=c)
	
	def save(self, request):
		return self.templates.empty()
	
	def cancel(self, request):
		return self.templates.underConstruction()
		
	def unCancel(self, request):
		return self.templates.underConstruction()
		
	def accept(self, request):
		return self.templates.underConstruction()
		
	def setTeam(self, request):
		return self.templates.underConstruction()
		
