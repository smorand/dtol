# -*- coding: utf-8 -*-
#
# This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
#

class User(object):
	'''
	User object in session
	'''

	def __init__(self, user):
		self.id = user.id
		self.login = user.login
		self.isadmin = user.isadmin == 1
		self.lang = user.lang
		self.packgraphique = user.packgraphique
		self.primarycolor = user.primarycolor
		self.secondarycolor = user.secondarycolor
		self.country = user.country
		self.email = user.email
		self.zoom = user.zoom
		self.cache = None
		
