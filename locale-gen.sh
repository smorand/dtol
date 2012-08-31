#!/bin/bash

cd src
locales=`( cd locale && ls )`

for locale in $locales; do
	python core/manage.py makemessages -v 2 -l $locale
done

