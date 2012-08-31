#!/bin/bash

#( for f in drop.sql structure.sql data.sql; do
#	cat sql/$f
#done ) | mysql -hmysql.alwaysdata.com -udtol -p -Ddtol_dt

cd src
PYTHONPATH=. python scm/dtol/manage.py loaddata ../sql/users.json
echo "Loading data"
mysql -udtol -pdtol -Ddtol < ../sql/data.sql
