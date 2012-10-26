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
	print "update lasteventid"
	DtGame.objects.filter(id=gameid).update(lasteventid=F('lasteventid')+1)
	game = DtGame.objects.get(id=gameid)
	lasteventid = game.lasteventid
	print "new lasteventid is %d" % (lasteventid)
	time.sleep(10)
	spawn = game.spawns()[1]
	spawn.lasteventid = lasteventid
	spawn.save()
	print "transaction over"
