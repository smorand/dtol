# -*- coding: utf-8 -*-
#
# This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
#

from os import listdir
from core.settings import APPLICATION_ROOT

def reloadActions():
	actions = {}
	for action in [ file.replace('.py', '') for file in listdir(APPLICATION_ROOT + '/' + __name__.replace('.', '/') + '/actions') if file != '__init__.py' and file[-4:] != '.pyc' ]:
		module = __import__(__name__ + '.actions.' + action, globals(), locals(), [ action ], -1).__dict__
		for key in module.keys():
			if key[:2] != '__':
				actions[key] = module[key]
	return actions

actions = reloadActions()
