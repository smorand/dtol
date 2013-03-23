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
		if 'constraint' in request.session: del request.session['constraint']
		c = {
			'users': self.userManager.getUsersExcept([request.session['user'].login]),
			'constraints': self.teamManager.getTeamConstraints()
		}
		return self.templates.response('challenge.edit', context=c)
	
	def save(self, request):
		if request.POST['constraint'] == -1:
			tc = request.session['constraint']
			del request.session['constraint']
			exts = tc.extensions
			del tc.extensions
			tc.save()
			tc.extensions = exts
			tc.save()
		else:
			tc = self.teamManager.getTeamConstraint(int(request.POST['constraint']))
		# TODO : Save challenge
		if request.POST['constraint'] == -1:
			tc.gamelink = game.id
			tc.save()
		if 'constraint' in request.session: del request.session['constraint']
		return self.templates.empty()
	
	def cancel(self, request):
		return self.templates.underConstruction()
		
	def unCancel(self, request):
		return self.templates.underConstruction()
		
	def accept(self, request):
		return self.templates.underConstruction()
		
	def setTeam(self, request):
		return self.templates.underConstruction()
		
