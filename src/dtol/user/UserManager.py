# -*- coding: utf-8 -*-
#
# This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
#

import core.settings
from dtol.user.User import User
from dtol.models import DtUser, DtSponsored, DtEmailChange, DtExtension
from hashlib import sha1
import commons
from django.utils.translation import ugettext as _
from datetime import datetime, timedelta

class UserManager(object):
	'''
	Manage user, authentication and data
	'''

	def connect(self, login, password):
		user = None
		users = DtUser.objects.filter(login=login, password=sha1(password).hexdigest(), active__gte=True)
		if users:
			dtuser = users[0]
			dtuser.connected = 1
			dtuser.save()
			user = User(users[0])
		return user
	
	def disconnect(self, userId):
		DtUser.objects.filter(id=userId).update(connected=0)
		
	def getUsersConnected(self):
		return DtUser.objects.filter(connected=1, lastconnection__gte=datetime.now()-timedelta(minutes=1)).order_by('login')
	
	def setLanguage(self, userId, lang):
		DtUser.objects.filter(id=int(userId)).update(lang=lang)
	
	def getUserInfo(self, login):
		user = None
		users = DtUser.objects.filter(login=login)
		if users:
			user = users[0]
		return user
	
	def getUsers(self):
		return DtUser.objects.all()
	
	def getUser(self, userId):
		return DtUser.objects.get(id=userId)
	
	def updateProfile(self, login, password=None, email=None, country=None, primarycolor=None, secondarycolor=None):
		user = self.getUserInfo(login)
		if password != None and len(password) > 0:
			user.password = sha1(password).hexdigest()
		if country != None and len(country) > 0:
			user.country = country
		if primarycolor != None and len(primarycolor) > 0:
			user.primarycolor = primarycolor
		if secondarycolor != None and len(secondarycolor) > 0:
			user.secondarycolor = secondarycolor
		user.save()
		
		if email != None and len(email) != 0:
			key = commons.randomstring(20)
			DtEmailChange(key=key, user=DtUser(id=user.id), email=email).save()
			body = _("EMAIL_CONFIRM_CHANGE_BODY_%s") % (core.settings.URL_ROOT + "/confirmemail/" + key)
			commons.sendmail(_("EMAIL_CONFIRM_CHANGE_SUBJECT"), [ email ], None, body)
		
		return User(user)
	
	def saveProfile(self, cid, login, password, country, primarycolor, secondarycolor, extensions):
		user = DtUser.objects.get(id=cid)
		if len(login) > 0:
			user.login = login
		if len(password) > 0:
			pwd = commons.randomstring(4, "abcdefghijklmnopqrstuvwxyz") + commons.randomstring(4, "0123456789")
			user.password = sha1(pwd).hexdigest()
			body = _("EMAIL_NEW_PASSWORD_BODY_%s") % (pwd)
			commons.sendmail(_("EMAIL_NEW_PASSWORD_SUBJECT"), [ user.email ], None, body)
		user.country = country
		user.primarycolor = primarycolor
		user.secondarycolor = secondarycolor
		user.extensions = DtExtension.objects.filter(id__in=extensions)
		user.save()
	
	def createProfile(self, login, password, email, country, primarycolor, secondarycolor, extensions):
		user = DtUser()
		user.login = login
		user.password = sha1(password).hexdigest()
		user.email = email
		user.country = country
		user.primarycolor = primarycolor
		user.secondarycolor = secondarycolor
		user.save()
		user.extensions = DtExtension.objects.filter(id__in=extensions)
		user.save()
		keyObj = DtSponsored.objects.filter(email=email)[0]
		keyObj.user = user
		key = keyObj.key
		keyObj.key = ''
		keyObj.save()
		DtEmailChange(key=key, user=DtUser(id=user.id), email=email).save()
		body = _("EMAIL_NEW_USER_BODY_%s") % (login)
		commons.sendmail(_("EMAIL_NEW_USER_SUBJECT"), [ core.settings.ADMINS[0][1] ], None, body)
	
	def getSponsoredKeyInfo(self, key):
		keys = DtSponsored.objects.filter(key=key)
		key = None
		if len(keys):
			key = keys[0]
		return key

	def loginExists(self, login):
		return len(DtUser.objects.filter(login=login)) > 0
	
	def emailExists(self, email):
		return len(DtUser.objects.filter(email=email)) > 0 or len(DtEmailChange.objects.filter(email=email)) > 0
	
	def generatePassword(self, email):
		user = DtUser.objects.filter(email=email)[0]
		pwd = commons.randomstring(4, "abcdefghijklmnopqrstuvwxyz") + commons.randomstring(4, "0123456789")
		user.password = sha1(pwd).hexdigest()
		user.save()
		body = _("PASSWORD_GENERATION_EMAIL_%s") % (pwd)
		commons.sendmail(_("PASSWORD_GENERATION_EMAIL_SUBJECT"), [ email ], None, body)
	
	def activate(self, userId, value):
		user = DtUser.objects.get(id=userId)
		user.active = value
		user.save()
		if value == 1:
			# Send an email when the account is unlocked
			body = _("EMAIL_ACCOUNT_UNLOCKED_BODY_%s") % core.settings.URL_ROOT
			commons.sendmail(_("EMAIL_ACCOUNT_UNLOCKED_SUBJECT"), [ user.email ], None, body)
	
	def confirmemail(self, key):
		emails = DtEmailChange.objects.filter(key=key)
		emailAddr = None
		if emails:
			email = emails[0]
			emailAddr = email.email
			email.user.email = emailAddr
			email.user.save()
			email.delete()
		return emailAddr
		
	def sponsor(self, user, email):
		key = commons.randomstring(20)
		DtSponsored(key=key, email=email, sponsor=DtUser(id=user.id)).save()
		body = _("EMAIL_SPONSOR_BODY_%(login)s_%(url)s") % { 'login': user.login, 'url': core.settings.URL_ROOT + "/register/" + key }
		commons.sendmail(_("EMAIL_SPONSOR_SUBJECT_%s") % (user.login), [ email ], [ core.settings.ADMINS[0][1] ], body)
