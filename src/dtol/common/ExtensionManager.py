# -*- coding: utf-8 -*-
#
# This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
#

from dtol.models import DtExtension

class ExtensionManager(object):
	'''
	Get information about extension, spawns and rooms
	'''

	def getExtensions(self):
		return DtExtension.objects.all()

