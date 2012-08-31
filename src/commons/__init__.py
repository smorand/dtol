# -*- coding: utf-8 -*-
#
# This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
#

import random
import smtplib
from email.mime.text import MIMEText
#from settings import ADMINS, SMTP_AUTH, STATIC_ROOT, APPLICATION_ROOT
import core.settings
from datetime import datetime, date, timedelta
from copy import copy
from os import listdir
from os.path import sep
import re

Countries = [ flag[:-4] for flag in listdir(core.settings.STATIC_ROOT + 'images/flags') ]
Countries.sort()

random.seed()

def randomstring(size, chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"):
	return "".join([ chars[random.randint(0, len(chars)-1)] for i in range(size) ])

def sendmail(subject, to, cc, body):
	msg = MIMEText(body, 'plain' ,'UTF-8')
	msg['Subject'] = '[ %s ] %s' % (core.settings.SMTP_AUTH['subjectheader'], subject)
	msg['From'] = '%s <%s>' % (core.settings.SMTP_AUTH['from'], core.settings.ADMINS[0][1])
	msg['To'] = ", ".join(to)
	msg['Message-Id'] = randomstring(50) + '@dtol'
	msg['Date'] = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0100")
	recipients = to[:]
	if (cc != None):
		msg['Cc'] = ", ".join(cc)
		recipients.extend(cc)
	
	s = smtplib.SMTP(host=core.settings.SMTP_AUTH['server'], port=core.settings.SMTP_AUTH['port'])
	if core.settings.SMTP_AUTH.has_key('username'):
		s.login(core.settings.SMTP_AUTH['username'], core.settings.SMTP_AUTH['password'])
	s.sendmail(core.settings.ADMINS[0][1], recipients, msg.as_string())
	s.quit()

def weekofyear(d):
	'''
	This function calculate on a date the week of year using the ISO method
	Weeks start on monday, and 4 january is always in the first week while
	28 december is always in the last week.
	'''
	if not type(d) is date:
		raise "This methodwork only on date object"
	weekOne = date(d.year, 1, 4) # This day is always in the first year
	week = (d+timedelta(weekOne.weekday()-d.weekday())-weekOne).days/7+1
	if week == 0: # Meaning this day is in the previous year
		week = weekofyear(date(d.year-1, 12, 28)) # This is day is always in the last week of the year
	return week

def permutateonplace(array):
	for i in range(len(array)):
		j = random.randint(0, i)
		if j != i: array[i], array[j] = array[j], array[i]
	return array
		
def permutatenewarray(array):
	return permutateonplace(array[:])

def loadresource(resource):
	data = {}
	with open(core.settings.APPLICATION_ROOT + sep + resource, 'r') as f:
		for line in f:
			if line[0] != ';':
				key, val = line.strip().split('=')
				key = key.strip()
				val = val.strip()
				data[key] = val
	return data
		
	
