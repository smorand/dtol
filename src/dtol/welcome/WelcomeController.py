# -*- coding: utf-8 -*-
#
# This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
#

from django.http import HttpResponse
from django.template import Context
from django.utils.translation import ugettext as _
from core.settings import LANGUAGES
from dtol.graphics import CreateSpawn
from core.controllers import CommonController
from dtol.common import Countries
from dtol.models import DtChat, DtUser
import re

class WelcomeController(CommonController):
	'''
	classdocs
	'''
	
	def _geturls(self):
		return [
			{ 'pattern': '^/?$', 'method': 'index' },
			{ 'pattern': '^welcome$', 'method': 'index' },
			{ 'pattern': '^user/connected$', 'method': 'connected', 'right': 'connected' },
			{ 'pattern': '^recvchat/([0-9]+)$$', 'method': 'recvchat', 'right': 'connected' },
			{ 'pattern': '^authenticate$', 'method': 'authenticate' },
			{ 'pattern': '^logout$', 'method': 'logout', 'right': 'connected' },
			{ 'pattern': '^sendchat$', 'method': 'sendchat', 'right': 'connected' },
			{ 'pattern': '^profile$', 'method': 'getprofile', 'right': 'connected' },
			{ 'pattern': '^profile/update$', 'method': 'updateprofile', 'right': 'connected' },
			{ 'pattern': '^lang$', 'method': 'setlang', 'right': 'connected' },
			{ 'pattern': '^sponsor/([a-zA-Z0-9-_@.]+)$', 'method': 'sponsor', 'right': 'connected' },
			{ 'pattern': '^register/([A-Z0-9]+)$', 'method': 'registerform' },
			{ 'pattern': '^register$', 'method': 'register' },
			{ 'pattern': '^confirmemail/([A-Z0-9]+)$', 'method': 'confirmemail', 'right': 'connected' },
			{ 'pattern': '^spawn/([a-z0-9]+)/([a-z0-9]+)$', 'method': 'drawspawn' },
			{ 'pattern': '^spawn/([a-z0-9]+)/([a-z0-9]+)/([a-z0-9]+)$', 'method': 'drawspawn' }
		]

	def index(self, request):
		response= HttpResponse()
		c={ 'languages': [ l[0] for l in LANGUAGES ] }
		if not 'user' in request.session or request.session['user'] == None:
			if request.COOKIES.has_key('login') and request.COOKIES.has_key('password'):
				user = self.userManager.connect(request.COOKIES['login'], request.COOKIES['password'])
				if user != None:
					request.session['user'] = user
					request.session['connected'] = True
					if user.isadmin:
						request.session['admin'] = True
					response.set_cookie('lang', user.lang, 315360000) # ten years
					c['welcome'] = _("WELCOME_%s") % request.session['user'].login
					t = self.templates.index
				else:
					c['PASSWORD_GENERATION_PROGRESS'] = _('PASSWORD_GENERATION_PROGRESS')
					t = self.templates.authentication
			else:
				c['PASSWORD_GENERATION_PROGRESS'] = _('PASSWORD_GENERATION_PROGRESS')
				t = self.templates.authentication
		else:
			c['welcome'] = _("WELCOME_%s") % request.session['user'].login
			t = self.templates.index
		
		response.write(t.render(Context(c)))
		return response
	
	def authenticate(self, request):
		response = HttpResponse()
		contextData = { 'PASSWORD_GENERATION_PROGRESS': _('PASSWORD_GENERATION_PROGRESS') }
		login = ""
		password = ""
		t = self.templates.authentication
			
		try:
			login = request.POST['login']
			password = request.POST['password']
		except:
			pass # This is managed later with emtpy login or password

		if len(login) == 0 or len(password) == 0:
			contextData['error'] = _("LOGIN_PASSWORD_EMPTY")
		else:
			user = self.userManager.connect(login, password)
			if user != None:
				request.session['user'] = user
				request.session['connected'] = True
				if user.isadmin:
					request.session['admin'] = True
				if request.POST.has_key('autoconnect') and request.POST['autoconnect'] == '1': # Auto connect for later connection
					response.set_cookie('login', login, 315360000) # ten years
					response.set_cookie('password', password, 315360000) # ten years
					response.set_cookie('lang', user.lang, 315360000) # ten years
				response.status_code = 301
				response['Location'] = '/'
			else:
				contextData['error'] = _("AUTHENTICATION_FAILURE")
			
		response.write(t.render(Context(contextData)))
		return response
	
	def logout(self, request):
		if 'user' in request.session:
			self.userManager.disconnect(request.session['user'].id)
			del request.session['user']
		if 'realuser' in request.session:
			del request.session['realuser']
		if 'connected' in request.session:
			del request.session['connected']
		response = HttpResponse(status=301)
		response['Location'] = '/'
		response.delete_cookie('login')
		response.delete_cookie('password')
		return response
	
	def recvchat(self, request, chatId):
		cid = None
		login = None
		if 'realuser' in request.session:
			cid = request.session['realuser'].id
			login = request.session['realuser'].login
		else:
			cid = request.session['user'].id
			login = request.session['user'].login
		messagesList = DtChat.objects.filter(id__gt=chatId).order_by('-id')[:50]
		messagesText = ''
		maxId = 0
		highlight = '0';
		for msg in messagesList:
			maxId = msg.id if msg.id > maxId else maxId
			if msg.user.id == cid:
				cls = 'chat-login-self'
			else:
				cls = 'chat-login'
			loginRegEx = re.compile(login, re.I)
			if loginRegEx.search(msg.message) != None:
				highlight = '1'
			message = loginRegEx.sub('<span class="chat-login-self">' + login + '</span>', msg.message)
			messagesText = '<br/><strong class="' + cls + '">' + msg.user.login + ':</strong> <strong class="chat-message">' + message + '</strong>' + messagesText
		return self.templates.content(str(maxId) + '|$|' + highlight + '|$|' + messagesText)

	def sendchat(self, request):
		message = request.POST['message']
		cid = None
		if 'realuser' in request.session:
			cid = request.session['realuser'].id
		else:
			cid = request.session['user'].id
		DtChat(user=DtUser(id=cid), message=message).save()
		return self.templates.empty()
	
	def listnews(self, request):
		return self.templates.underConstruction()
	
	def createnews(self, request):
		return self.templates.underConstruction()
	
	def deletenews(self, request):
		return self.templates.underConstruction()
	
	def connected(self, request):
		return self.templates.response('connected', context={ 'users': ",".join([ user.login for user in self.userManager.getUsersConnected() ]) })
	
	def getprofile(self, request):
		return self.templates.response('view_profile', context={ 'user': request.session['user'], 'countries': Countries })
	
	def setlanguage(self, request):
		lang = request.POST['lang'].strip()
		if request.session.has_key('user'):
			self.userManager.setLanguage(request.session['user'].id, lang)
		response = HttpResponse('')
		response.set_cookie('lang', lang, 315360000) # ten years
		return response

	def updateprofile(self, request):
		errors = []
		password = request.POST['password']
		if len(password) != 0 and password != request.POST['confirmpassword']:
			errors.append(_("PASSWORD_DIFFERS"))
		email = request.POST['email']
		if email == request.session['user'].email:
			email = None
		elif self.userManager.emailExists(email):
			email = None
			errors.append(_("EMAIL_EXISTS"))
		country = request.POST['country']
		if country not in Countries:
			errors.append(_("COUNTRY_DOES_NOT_EXIST"))
		primarycolor = request.POST['primarycolor']
		secondarycolor = request.POST['secondarycolor']
		if len(errors) == 0:
			request.session['user'] = self.userManager.updateProfile(request.session['user'].login, password, email, country, primarycolor, secondarycolor)
			c = { 'notice': _("UPDATE_PROFILE_OK") }
		else:
			c = { 'errors': errors }
		return self.templates.response('message_return', context=c)

	def sponsor(self, request, email):
		if self.userManager.emailExists(email):
			c = { 'error': _("EMAIL_EXISTS") }
		else:
			self.userManager.sponsor(request.session['user'], email)
			c = { 'notice': _("SPONSORING_OK") }
		return self.templates.response('message_return', context=c)
	
	def confirmemail(self, request, key):
		email = self.userManager.confirmemail(key)
		if email != None and 'user' in request.session:
			request.session['user'].email = email 
		return self.templates.redirect('/')
	
	def registerform(self, request, key):
		keyInfo = self.userManager.getSponsoredKeyInfo(key)
		
		extensions = self.extensionManager.getExtensions()
		c = {
			'languages': [ l[0] for l in LANGUAGES ],
			'countries': Countries,
			'extensions': extensions,
			'key': keyInfo.key if keyInfo != None else '*'
		}
		return self.templates.response('register', context=c)
		
	def register(self, request):
		errors = []
		
		key = request.POST['key']
		keyInfo = self.userManager.getSponsoredKeyInfo(key)
		
		if keyInfo == None:
			errors.append(_("KEY_INACTIVE"))
		elif keyInfo.sponsor.active != 1:
			errors.append(_("SPONSOR_SUSPENDED"))
		else:
			email = keyInfo.email
		
		login = request.POST['login']
		if self.userManager.loginExists(login):
			errors.append(_("LOGIN_ALREADY_TAKEN"))
		
		password = request.POST['password']
		if len(password) == 0:
			errors.append(_("PASSWORD_NULL"))
		elif password != request.POST['confirmpassword']:
			errors.append(_("PASSWORD_DIFFERS"))
		
		country = request.POST['country']
		if country not in Countries:
			errors.append(_("COUNTRY_DOES_NOT_EXIST"))
		
		primarycolor = request.POST['primarycolor']
		secondarycolor = request.POST['secondarycolor']
		
		extensions = request.POST['extensions'].split(',')
		
		if len(errors) == 0:
			request.session['user'] = self.userManager.createProfile(login, password, email, country, primarycolor, secondarycolor, extensions)
			c = { 'notice': _("REGISTER_OK") }
		else:
			c = { 'errors': errors }
		
		return self.templates.response('message_return', context=c)
	
	def drawspawn(self, request, fond, spawn, marker=None):
		markers = []
		if not marker is None:
			markers.append(marker)
		return HttpResponse(CreateSpawn(fond, spawn, markers), mimetype='image/png')
