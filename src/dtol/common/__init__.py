# -*- coding: utf-8 -*-
#
# This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
#

from  core.controllers import PreHandler
from dtol.models import DtUser
import datetime
import os
from core.settings import STATIC_ROOT

Countries = [ flag[:-4] for flag in os.listdir(STATIC_ROOT +  'images' + os.path.sep + 'flags') ]
Countries.sort()

class PreHandlerConnect(PreHandler):
	def handle(self, request):
		cid = None
		if 'realuser' in request.session and request.session['realuser'] != None:
			cid = request.session['realuser'].id
		elif 'user' in request.session and request.session['user'] != None:
			cid = request.session['user'].id
		if cid != None:
			DtUser.objects.filter(id=cid).update(lastconnection=datetime.datetime.now())

