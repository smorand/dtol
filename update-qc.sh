#!/bin/bash

rsync -av --delete src/ app01:/home/dtol --exclude *.po --exclude *.pyc
ssh app01 chgrp www-data /home/dtol -R
ssh app01 chmod g+w /home/dtol/resources/dtol.db
ssh app01 sudo /etc/init.d/apache2 restart
