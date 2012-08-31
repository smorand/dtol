#!/bin/bash

cd src
locales=`( cd locale && ls )`

for locale in $locales; do
	python core/manage.py compilemessages -v 2 -l $locale
done

