# -*- coding: utf-8 -*-
#
# This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
#

from core.controllers import CommonController
from dtol.models import DtTeamConstraint, DtTeamConstraintExtension, DtExtension
from django.utils.translation import ugettext as _

class TeamController(CommonController):
	'''
	Manage team
	'''
	
	def _geturls(self):
		return [
			{ 'pattern': r'^teams$', 'method': 'list' },
			{ 'pattern': r'^teams/constraints$', 'method': 'listconstraints' },
			{ 'pattern': r'^teams/constraints/edit/([0-9]+)$', 'method': 'createconstraints' },
			{ 'pattern': r'^teams/constraints/remove/([1-9][0-9]*)$', 'method': 'delteamsconstraints' },
			{ 'pattern': r'^teams/constraints/load/([1-9][0-9]*)$', 'method': 'loadteamsconstraint' },
			{ 'pattern': r'^teams/constraints/save$', 'method': 'saveteamsconstraint' },
		]

	def list(self, request):
		''' List teams: teams used for a game are excluded '''
		c = {
			'teams': self.teamManager.getTeams(user=request.session['user']),
			'constraints': self.teamManager.getTeamConstraints()
		}
		return self.templates.response('team.list', context=c)
	
	def listconstraints(self, request):
		''' List teams constraints. Only available for some users '''
		c = {
			'constraints': self.teamManager.getTeamConstraints()
		}
		return self.templates.response('team.listconstraints', context=c)

	def delteamsconstraints(self, request, uid):
		''' Remove a team constraint Protected constraint can't be removed. This is a logical deletion '''
		self.teamManager.delTeamConstraint(uid)
		return self.templates.empty()
	
	def createconstraints(self, request, uid):
		''' Load page for edit/create constraint '''
		tc = DtTeamConstraint(id=0, name='', game=None) if uid == '0' else self.teamManager.getTeamConstraint(uid)
		c = {
			'constraints': self.teamManager.getTeamConstraints(),
			'constraint': tc,
			'extensionslist': self.extensionManager.getExtensions(),
			'new': uid == 0
		}
		c['extensions'] = ",".join([ str(ext.id) for ext in tc.extensions.all() ])
		return self.templates.response('team.createconstraint', context=c)

	def loadteamsconstraint(self, request, uid):
		''' Load a team constraint to reload document '''
		c = {
			'constraint': self.teamManager.getTeamConstraint(uid),
		}
		return self.templates.response('team.loadteamconstraint', context=c)

	def saveteamsconstraint(self, request):
		''' Save teams constraints '''
		try:
			if 'name' not in request.POST or request.POST['name'] == '':
				raise Exception(_('TEAM_CONSTRAINT_EMPTY_NAME'))
			if 'id' in request.POST and request.POST['id'] != '0' and request.POST['id'] != '':
				tc = self.teamManager.getTeamConstraint(request.POST['id'])
				tc.name = request.POST['name']
			else:
				tc = DtTeamConstraint(name=request.POST['name'])
			try: tc.mincharacters = int(request.POST['mincharacters'])
			except: raise Exception('INCORRECT_VALUE_MINCHARACTERS')
			try: tc.maxcharacters = int(request.POST['maxcharacters'])
			except: raise Exception('INCORRECT_VALUE_MAXCHARACTERS')
			try: tc.minobjects = int(request.POST['minobjects'])
			except: raise Exception('INCORRECT_VALUE_MINOBJECTS')
			try: tc.maxobjects = int(request.POST['maxobjects'])
			except: raise Exception('INCORRECT_VALUE_MAXOBJECTS')
			try: tc.minrooms = int(request.POST['minrooms'])
			except: raise Exception('INCORRECT_VALUE_MINROOMS')
			try: tc.maxrooms = int(request.POST['maxrooms'])
			except: raise Exception('INCORRECT_VALUE_MAXROOMS')
			try: tc.mindeplacement = int(request.POST['mindeplacement'])
			except: raise Exception('INCORRECT_VALUE_MINDEPLACEMENT')
			try: tc.maxdeplacement = int(request.POST['maxdeplacement'])
			except: raise Exception('INCORRECT_VALUE_MAXDEPLACEMENT')
			try: tc.mintotaldeplacement = int(request.POST['mintotaldeplacement'])
			except: raise Exception('INCORRECT_VALUE_MINTOTALDEPLACEMENT')
			try: tc.maxtotaldeplacement = int(request.POST['maxtotaldeplacement'])
			except: raise Exception('INCORRECT_VALUE_MAXTOTALDEPLACEMENT')
			try: tc.minadvdeplacement = int(request.POST['minadvdeplacement'])
			except: raise Exception('INCORRECT_VALUE_MINADVDEPLACEMENT')
			try: tc.maxadvdeplacement = int(request.POST['maxadvdeplacement'])
			except: raise Exception('INCORRECT_VALUE_MAXADVDEPLACEMENT')
			try: tc.mintotaladvdeplacement = int(request.POST['mintotaladvdeplacement'])
			except: raise Exception('INCORRECT_VALUE_MINTOTALADVDEPLACEMENT')
			try: tc.maxtotaladvdeplacement = int(request.POST['maxtotaladvdeplacement'])
			except: raise Exception('INCORRECT_VALUE_MAXTOTALADVDEPLACEMENT')
			try: tc.minforce = int(request.POST['minforce'])
			except: raise Exception('INCORRECT_VALUE_MINFORCE')
			try: tc.maxforce = int(request.POST['maxforce'])
			except: raise Exception('INCORRECT_VALUE_MAXFORCE')
			try: tc.mintotalforce = int(request.POST['mintotalforce'])
			except: raise Exception('INCORRECT_VALUE_MINTOTALFORCE')
			try: tc.maxtotalforce = int(request.POST['maxtotalforce'])
			except: raise Exception('INCORRECT_VALUE_MAXTOTALFORCE')
			try: tc.minprestigious = int(request.POST['minprestigious'])
			except: raise Exception('INCORRECT_VALUE_MINPRESTIGIOUS')
			try: tc.maxprestigious = int(request.POST['maxprestigious'])
			except: raise Exception('INCORRECT_VALUE_MAXPRESTIGIOUS')
			try: tc.minspellcaster = int(request.POST['minspellcaster'])
			except: raise Exception('INCORRECT_VALUE_MINSPELLCASTER')
			try: tc.maxspellcaster = int(request.POST['maxspellcaster'])
			except: raise Exception('INCORRECT_VALUE_MAXSPELLCASTER')
			try: tc.minflying = int(request.POST['minflying'])
			except: raise Exception('INCORRECT_VALUE_MINFLYING')
			try: tc.maxflying = int(request.POST['maxflying'])
			except: raise Exception('INCORRECT_VALUE_MAXFLYING')
			try: tc.minintangible = int(request.POST['minintangible'])
			except: raise Exception('INCORRECT_VALUE_MININTANGIBLE')
			try: tc.maxintangible = int(request.POST['maxintangible'])
			except: raise Exception('INCORRECT_VALUE_MAXINTANGIBLE')
			try: tc.mincursed = int(request.POST['mincursed'])
			except: raise Exception('INCORRECT_VALUE_MINCURSED')
			try: tc.maxcursed = int(request.POST['maxcursed'])
			except: raise Exception('INCORRECT_VALUE_MAXCURSED')
			try: tc.minshadowwalker = int(request.POST['minshadowwalker'])
			except: raise Exception('INCORRECT_VALUE_MINSHADOWWALKER')
			try: tc.maxshadowwalker = int(request.POST['maxshadowwalker'])
			except: raise Exception('INCORRECT_VALUE_MAXSHADOWWALKER')
			try: tc.minshadowroom = int(request.POST['minshadowroom'])
			except: raise Exception('INCORRECT_VALUE_MINSHADOWROOM')
			try: tc.maxshadowroom = int(request.POST['maxshadowroom'])
			except: raise Exception('INCORRECT_VALUE_MAXSHADOWROOM')
			try: tc.minantimagicroom = int(request.POST['minantimagicroom'])
			except: raise Exception('INCORRECT_VALUE_MINANTIMAGICROOM')
			try: tc.maxantimagicroom = int(request.POST['maxantimagicroom'])
			except: raise Exception('INCORRECT_VALUE_MAXANTIMAGICROOM')
			try: tc.minfountain = int(request.POST['minfountain'])
			except: raise Exception('INCORRECT_VALUE_MINFOUNTAIN')
			try: tc.maxfountain = int(request.POST['maxfountain'])
			except: raise Exception('INCORRECT_VALUE_MAXFOUNTAIN')
			try: tc.mincounterfountain = int(request.POST['mincounterfountain'])
			except: raise Exception('INCORRECT_VALUE_MINCOUNTERFOUNTAIN')
			try: tc.maxcounterfountain = int(request.POST['maxcounterfountain'])
			except: raise Exception('INCORRECT_VALUE_MAXCOUNTERFOUNTAIN')
			try: tc.minextensions = int(request.POST['minextensions'])
			except: raise Exception('INCORRECT_VALUE_MINEXTENSIONS')
			try: tc.maxextensions = int(request.POST['maxextensions'])
			except: raise Exception('INCORRECT_VALUE_MAXEXTENSIONS')
			try: tc.maxsamecharacter = int(request.POST['maxsamecharacter'])
			except: raise Exception('INCORRECT_VALUE_MAXSAMECHARACTER')
			try: tc.maxsameobject = int(request.POST['maxsameobject'])
			except: raise Exception('INCORRECT_VALUE_MAXSAMEOBJECT')
			try: tc.maxcommonobject = int(request.POST['maxcommonobject'])
			except: raise Exception('INCORRECT_VALUE_MAXCOMMONOBJECT')
			try: tc.maxsameroom = int(request.POST['maxsameroom'])
			except: raise Exception('INCORRECT_VALUE_MAXSAMEROOM')
			tc.mincharacters = tc.mincharacters if tc.mincharacters >= 0 else -1
			tc.maxcharacters = tc.maxcharacters if tc.maxcharacters >= 0 else -1
			tc.minobjects = tc.minobjects if tc.minobjects >= 0 else -1
			tc.maxobjects = tc.maxobjects if tc.maxobjects >= 0 else -1
			tc.minrooms = tc.minrooms if tc.minrooms >= 0 else -1
			tc.maxrooms = tc.maxrooms if tc.maxrooms >= 0 else -1
			tc.mindeplacement = tc.mindeplacement if tc.mindeplacement >= 0 else -1
			tc.maxdeplacement = tc.maxdeplacement if tc.maxdeplacement >= 0 else -1
			tc.mintotaldeplacement = tc.mintotaldeplacement if tc.mintotaldeplacement >= 0 else -1
			tc.maxtotaldeplacement = tc.maxtotaldeplacement if tc.maxtotaldeplacement >= 0 else -1
			tc.minadvdeplacement = tc.minadvdeplacement if tc.minadvdeplacement >= 0 else -1
			tc.maxadvdeplacement = tc.maxadvdeplacement if tc.maxadvdeplacement >= 0 else -1
			tc.mintotaladvdeplacement = tc.mintotaladvdeplacement if tc.mintotaladvdeplacement >= 0 else -1
			tc.maxtotaladvdeplacement = tc.maxtotaladvdeplacement if tc.maxtotaladvdeplacement >= 0 else -1
			tc.minforce = tc.minforce if tc.minforce >= 0 else -1
			tc.maxforce = tc.maxforce if tc.maxforce >= 0 else -1
			tc.mintotalforce = tc.mintotalforce if tc.mintotalforce >= 0 else -1
			tc.maxtotalforce = tc.maxtotalforce if tc.maxtotalforce >= 0 else -1
			tc.minprestigious = tc.minprestigious if tc.minprestigious >= 0 else -1
			tc.maxprestigious = tc.maxprestigious if tc.maxprestigious >= 0 else -1
			tc.minspellcaster = tc.minspellcaster if tc.minspellcaster >= 0 else -1
			tc.maxspellcaster = tc.maxspellcaster if tc.maxspellcaster >= 0 else -1
			tc.minflying = tc.minflying if tc.minflying >= 0 else -1
			tc.maxflying = tc.maxflying if tc.maxflying >= 0 else -1
			tc.minintangible = tc.minintangible if tc.minintangible >= 0 else -1
			tc.maxintangible = tc.maxintangible if tc.maxintangible >= 0 else -1
			tc.mincursed = tc.mincursed if tc.mincursed >= 0 else -1
			tc.maxcursed = tc.maxcursed if tc.maxcursed >= 0 else -1
			tc.minshadowwalker = tc.minshadowwalker if tc.minshadowwalker >= 0 else -1
			tc.maxshadowwalker = tc.maxshadowwalker if tc.maxshadowwalker >= 0 else -1
			tc.minshadowroom = tc.minshadowroom if tc.minshadowroom >= 0 else -1
			tc.maxshadowroom = tc.maxshadowroom if tc.maxshadowroom >= 0 else -1
			tc.minantimagicroom = tc.minantimagicroom if tc.minantimagicroom >= 0 else -1
			tc.maxantimagicroom = tc.maxantimagicroom if tc.maxantimagicroom >= 0 else -1
			tc.minfountain = tc.minfountain if tc.minfountain >= 0 else -1
			tc.maxfountain = tc.maxfountain if tc.maxfountain >= 0 else -1
			tc.mincounterfountain = tc.mincounterfountain if tc.mincounterfountain >= 0 else -1
			tc.maxcounterfountain = tc.maxcounterfountain if tc.maxcounterfountain >= 0 else -1
			tc.minextensions = tc.minextensions if tc.minextensions >= 0 else -1
			tc.maxextensions = tc.maxextensions if tc.maxextensions >= 0 else -1
			tc.maxsamecharacter = tc.maxsamecharacter if tc.maxsamecharacter >= 0 else -1
			tc.maxsameobject = tc.maxsameobject if tc.maxsameobject >= 0 else -1
			tc.maxcommonobject = tc.maxcommonobject if tc.maxcommonobject >= 0 else -1
			tc.maxsameroom = tc.maxsameroom if tc.maxsameroom >= 0 else -1
			tc.save()
			if 'extensions' in request.POST and request.POST['extensions'] != '':
				for ext in request.POST['extensions'].strip().split(','):
					DtTeamConstraintExtension(teamconstraint=tc	, extension=DtExtension(id=int(ext))).save()
		except Exception as err:
			return self.templates.response('message_return', context={ 'error': str(err)})
		return self.templates.empty()

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
	
	
