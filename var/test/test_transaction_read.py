#!/usr/bin/env python

import time
import sys
from django.conf import settings

settings.configure(
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.mysql',
			'NAME': 'test',
			'USER': 'test',
			'PASSWORD': 'test',
			'HOST': 'localhost'
		}
	}
)

from essai.models import DtGame
from django.db import transaction
from django.db.models import F

with transaction.commit_on_success():
	gameid = int(sys.argv[1])
	print "work on game %d" % (gameid)
	lasteventidplayer = int(sys.argv[2])
	print "lock read game"
	game = DtGame.objects.select_for_update().filter(id=gameid)[0]
	print "lasteventid of game is %d" % (game.lasteventid)
	print [ (sp.name, sp.lasteventid) for sp in game.spawns(lasteventidplayer) ]
