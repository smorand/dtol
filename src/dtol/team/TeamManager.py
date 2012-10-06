# -*- coding: utf-8 -*-
#
# This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
#

from dtol.models import DtTeam, DtTeamConstraint

class TeamManager(object):
	'''
	Manage user, authentication and data
	'''

	def getTeams(self, user):
		return DtTeam.objects.filter(user=user.id)

	def getTeamConstraints(self, protected=None, game=None):
		kwargs = { 'deleted': 0 }
		if protected is not None:
			kwargs['protected'] = protected
		kwargs['game'] = game
		return DtTeamConstraint.objects.filter(**kwargs)

	def delTeamConstraint(self, uid):
		DtTeamConstraint.objects.filter(id=uid).update(deleted=1)
	
	def getTeamConstraint(self, uid):
		return DtTeamConstraint.objects.get(id=uid)
		