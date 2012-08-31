#!/bin/bash

pwd | grep -qE 'src$' && cd ..
rsync -av --delete src/ dtol@ssh.alwaysdata.com:dt --exclude *.po --exclude *.pyc --exclude rooms
echo "Set up new settings"
ssh dtol@ssh.alwaysdata.com cp dt/scm/dtol/settings.py.alwaysdata dt/scm/dtol/settings.py

