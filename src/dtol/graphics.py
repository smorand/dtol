# -*- coding: utf-8 -*-
#
# This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
#

from core.settings import STATIC_ROOT

'''
from PythonMagick import Image, Blob
from PythonMagick._PythonMagick import CompositeOperator

def CreateSpawn(fondColor, spawnName, markers=[]):
	# Create a character spawn with the provided markers in the asked color. The PNG data are returned
	spawn = Image(str(MEDIA_ROOT + '/images/spawns/fond-' + fondColor + '.png'))
	spawn.composite(Image(str(MEDIA_ROOT + '/images/spawns/' + spawnName + '.png')), 0, 0, CompositeOperator.OverCompositeOp)
	for marker in markers:
		spawn.composite(Image(str(MEDIA_ROOT + '/images/markers/' + marker + '.png')), 0, 0, CompositeOperator.OverCompositeOp)
	blob = Blob()
	spawn.write(blob)
	return blob.data
'''

from os import system
from tempfile import mkstemp
import string

def CreateSpawn(fondColor, spawnName, markers=[]):
	info = mkstemp(prefix='dtol')
	outputFileName = info[1]
	system('composite ' + STATIC_ROOT + 'images/spawns/' + spawnName + '.png ' + STATIC_ROOT + 'images/spawns/fond-' + fondColor + '.png ' + outputFileName)
	for marker in markers:
		system('composite ' + STATIC_ROOT + 'images/markers/' + marker + '.png ' + outputFileName + ' ' + outputFileName)
	with open(outputFileName, 'r') as f: data = f.read()
	return data
