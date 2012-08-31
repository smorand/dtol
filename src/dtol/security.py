# -*- coding: utf-8 -*-
#
# This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
#

from settings import APPLICATION_ROOT

class SecurityHelper(object):
	'''
	This class test security of the request
	'''
	
	def after_properties_set(self):
		print APPLICATION_ROOT + "/resources/" + self.securityFile
		self._security = {}
		f = open(APPLICATION_ROOT + "/resources/" + self.securityFile, 'r')
		line = f.readline()
		if line != '':
			line = line.strip()
			key, rolesString = line.split('=')
			roles = [ role.strip() for role in rolesString.split(',') if len(role.strip()) > 0 ]
			if len(roles) > 0:
				if not self._security.has_key(key):
					self._security[key] = []
				self._security[key].extend(roles)

	def check(self, controller, request):
		user = request.session.get('user', default=None)
		check = True
		if self._security.has_key(controller):
			check = False
			if user != None:
				for role in user.roles:
					if role in self._security[controller]:
						check = True
						break

		return check
		
