# -*- coding: utf-8 -*-
#
# This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
#

from dtol.models import DtExtension

class ExtensionManager(object):
	'''
	Get information about extension, spawns and rooms
	'''

	def getExtensions(self, extensions=None):
		return DtExtension.objects.all() if extensions is None or len(extensions.all()) == 0 else extensions.all()

