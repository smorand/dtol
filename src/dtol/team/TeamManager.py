# -*- coding: utf-8 -*-
#
# This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
#

from dtol.models import DtTeam

class TeamManager(object):
	'''
	Manage user, authentication and data
	'''

	def getTeams(self, user):
		return DtTeam.objects.filter(user=user.id)
