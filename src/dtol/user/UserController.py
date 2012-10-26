# -*- coding: utf-8 -*-
#
# This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
#

from django.utils.translation import ugettext as _
from core.controllers import CommonController
from dtol.common import Countries
from dtol.user.User import User

class UserController(CommonController):
	'''
	Manage the administration part
	'''
	
	def _geturls(self):
		return [
			{ 'pattern': r'^admin$', 'method': 'list' },
			{ 'pattern': r'^user/unblock/([0-9]+)$', 'method': 'unblock' },
			{ 'pattern': r'^user/block/([0-9]+)$', 'method': 'block' },
			{ 'pattern': r'^user/view/([0-9]+)$', 'method': 'view' },
			{ 'pattern': r'^user/update$', 'method': 'update' },
			{ 'pattern': r'^user/become/([0-9]+)$', 'method': 'become' },
			{ 'pattern': r'^generatepassword$', 'method': 'generatepassword' },
		]

	def list(self, request):
		return self.templates.response('user_list', context={ 'users': self.userManager.getUsers() })
		
	def view(self, request, userId):
		extensions = self.extensionManager.getExtensions()
		user = self.userManager.getUser(userId)
		return self.templates.response('view_user', context={ 'countries': Countries, 'extensions': extensions, 'user': user, 'userExtensions': ",".join([ str(ext.id) for ext in user.extensions.all() ]) })
		
	def update(self, request):
		errors = []
		cid = int(request.POST['id'])
		login = request.POST['login']
		userLogin = self.userManager.getUserInfo(login)
		if userLogin != None and userLogin.id != cid:
			errors.append(_("LOGIN_ALREADY_TAKEN"))
			
		password = request.POST['password']

		country = request.POST['country']
		if country not in Countries:
			errors.append(_("COUNTRY_DOES_NOT_EXIST"))
			
		primarycolor = request.POST['primarycolor']
		secondarycolor = request.POST['secondarycolor']
		
		extensions = request.POST['extensions'].strip()
		if len(extensions) == 0:
			extensions = []
		else:
			extensions = extensions.split(',')

		if len(errors) == 0:
			self.userManager.saveProfile(cid, login, password, country, primarycolor, secondarycolor, extensions)
			c = { 'notice': _("SAVE_USER_OK") }
		else:
			c = { 'errors': errors }

		return self.templates.response('message_return', context=c)
		
	def block(self, request, userId):
		self.userManager.activate(userId, 0)
		return self.templates.response('message_return', context={ 'notice': _("BLOCK_DONE")})
		
	def unblock(self, request, userId):
		self.userManager.activate(userId, 1)
		return self.templates.response('message_return', context={ 'notice': _("UNBLOCK_DONE")})
	
	def generatepassword(self, request):
		if self.userManager.emailExists(request.POST['email']):
			self.userManager.generatePassword(request.POST['email'])
			c={ 'notice': _("PASSWORD_GENERATION_DONE") }
		else:
			c={ 'error': _("PASSWORD_GENERATION_INVALID_EMAIL") }
		return self.templates.response('message_return', c)
	
	def become(self, request, userId):
		if not 'realuser' in request.session:
			request.session['realuser'] = request.session['user']
		request.session['user'] = User(self.userManager.getUser(userId))  
		return self.templates.response('message_return')
