# -*- coding: utf-8 -*-
#
# This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
#

from django import template

register = template.Library()

def key(d, key_name):
	try:
		value = d[key_name]
	except:
		from django.conf import settings
		value = settings.TEMPLATE_STRING_IF_INVALID
	return value

key = register.filter('key', key)
