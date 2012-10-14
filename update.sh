#!/bin/bash

pwd | grep -qE 'src$' && cd ..
rsync -av --delete src/ dtol@ssh.alwaysdata.com:dt --exclude *.po --exclude *.pyc --exclude rooms
#ssh app01 chgrp www-data dt -R
ssh dtol@ssh.alwaysdata.com chmod go+w dt/resources/dtol.db
