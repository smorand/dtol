# -*- coding: utf-8 -*-
#
# This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
#

from dtol.models import DtCharacter, DtObject, DtRoom

class SpawnManager(object):
	'''
	Manage the spawns
	'''

	def getCharacters(self, extensions):
		return DtCharacter.objects.filter(extensions__in=extensions).distinct()
	
	def getObjects(self, extensions):
		return DtObject.objects.filter(extensions__in=extensions).distinct()

	def getRooms(self, extensions):
		return DtRoom.objects.filter(extensions__in=extensions).distinct()

	def getCharacter(self, sid):
		return DtCharacter.objects.get(id=sid)
	
	def getObject(self, sid):
		return DtObject.objects.get(id=sid)

	def getRoom(self, sid):
		return DtRoom.objects.get(id=sid)