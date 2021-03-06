# -*- coding: utf-8 -*-
#
# This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
#

from dtol.models import DtTeam, DtTeamConstraint
from django.utils.translation import ugettext as _
import random, math

class TeamManager(object):
	'''
	Manage user, authentication and data
	'''

	def getTeams(self, user):
		return DtTeam.objects.filter(user=user.id)

	def getTeamConstraints(self, user=None):
		if user is None:
			where = [ 'deleted = 0 and public = 1 and gamelink = 0' ]
		else:
			where = [ 'deleted = 0 and (public = 1 or user_id = %d) and gamelink = 0' % (user) ]
		return DtTeamConstraint.objects.extra(where=where)

	def delTeamConstraint(self, uid, user):
		if user is None:
			DtTeamConstraint.objects.filter(id=uid).update(deleted=1)
		else:
			DtTeamConstraint.objects.filter(id=uid, user=user).update(deleted=1)

	def delTeam(self, uid):
		DtTeam.objects.filter(id=uid).delete()
	
	def getTeamConstraint(self, uid):
		return DtTeamConstraint.objects.get(id=uid)
	
	def getTeamFilter(self, extensions):
		characters = []
		objects = []
		rooms = []
		for c in self.spawnManager.getCharacters(extensions):
			sp = {
				'id': c.id,
				'name': c.name,
				'force': c.force,
				'deplacement': c.deplacement,
				'extensions': '-'.join([ str(e.id) for e in c.extensions.all() ]),
				'filters': []
			}
			capacities = list()
			for cap in c.capacities():
				capinfo = cap.name.split('_')
				if capinfo[0] == 'walker' or capinfo[0] == 'biendans':
					for capinfo2 in capinfo[1].split('-'):
						capacities.append('%s_%s' % (capinfo[0], capinfo2))
				elif cap.name.find('regenerater') > 0:
					capacities.append(capinfo[0])
				else:
					capacities.append(capinfo[0])
			if c.advdeplacement() >= 5: sp['filters'].append('runner')
			if c.advforce() >= 3: sp['filters'].append('fighter')
			if 'spellcaster' in capacities: sp['filters'].append('spellcaster')
			if 'flyer' in capacities: sp['filters'].append('flyer')
			if 'regenerater' in capacities: sp['filters'].append('regenerater')
			if 'prestigious' in capacities: sp['filters'].append('prestigious')
			if 'undead' in capacities: sp['filters'].append('undead')
			if 'immaterial' in capacities: sp['filters'].append('immaterial')
			if 'walker_tenebres' in capacities: sp['filters'].append('walker_tenebres')
			if 'walker_tenebresmagiques' in capacities: sp['filters'].append('walker_tenebres')
			if 'elf' in capacities: sp['filters'].append('elf')
			if 'dwarf' in capacities: sp['filters'].append('dwarf')
			if 'beast' in capacities: sp['filters'].append('beast')
			if 'antifountain' in capacities: sp['filters'].append('antifountain')
			if 'biendans_eau' in capacities: sp['filters'].append('biendans_eau')
			if 'biendans_lave' in capacities: sp['filters'].append('biendans_lave')
			sp['filters'] = '-'.join(sp['filters']) 
			characters.append(sp)
		for c in self.spawnManager.getObjects(extensions):
			sp = {
				'id': c.id,
				'name': c.name,
				'extensions': '-'.join([ str(e.id) for e in c.extensions.all() ]),
				'filters': []
			}
			capacities = [ cap.name for cap in c.capacities() ]
			if 'categorie_current' in capacities: sp['filters'].append('current')
			if 'magical' in capacities: sp['filters'].append('magical')
			if 'parchemin' in capacities: sp['filters'].append('parchemin')
			if 'categorie_arme' in capacities: sp['filters'].append('categorie_arme')
			if 'shield' in capacities: sp['filters'].append('shield')
			if 'categorie_puissant' in capacities: sp['filters'].append('categorie_puissant')
			if 'antifountain' in capacities: sp['filters'].append('antifountain')
			if 'categorie_cursed' in capacities: sp['filters'].append('cursed')
			if 'parchemin' in capacities: sp['filters'].append('perchemin')
			if 'categorie_arme' in capacities: sp['filters'].append('weapon')
			sp['filters'] = '-'.join(sp['filters'])
			objects.append(sp)
		for c in self.spawnManager.getRooms(extensions):
			sp = {
				'id': c.id,
				'name': '%s-%d' % (c.number, c.rotation),
				'extensions': '-'.join([ str(e.id) for e in c.extensions.all() ]),
				'filters': []
			}
			capacities = [ cap.name for cap in c.categories.all() ]
			if 'tenebres' in capacities: sp['filters'].append('tenebres')				
			if 'eau' in capacities: sp['filters'].append('eau')
			if 'lave' in capacities: sp['filters'].append('lave')
			if 'fontaine' in capacities: sp['filters'].append('fontaine')
			if 'pente' in capacities: sp['filters'].append('pente')
			if 'neige' in capacities: sp['filters'].append('neige')
			if 'brume' in capacities: sp['filters'].append('brume')
			if 'arbre' in capacities: sp['filters'].append('arbre')
			if 'torche' in capacities: sp['filters'].append('torche')
			sp['filters'] = '-'.join(sp['filters'])
			rooms.append(sp)
		return characters, objects, rooms

	def getTeam(self, teamid):
		return DtTeam.objects.get(id=teamid)

	@staticmethod
	def checkTeamConstraintCharacters(constraintin, characters):
		errors = list()
		if type(constraintin) != DtTeamConstraint:
			constraint = DtTeamConstraint.objects.get(id=constraintin)
		else:
			constraint = constraintin
		if constraint.mincharacters != -1 and constraint.mincharacters > len(characters): errors.append(_('CONSTRAINT_CHECK_NOT_ENOUGH_CHARACTER'))
		if constraint.maxcharacters != -1 and constraint.maxcharacters < len(characters): errors.append(_('CONSTRAINT_CHECK_TOO_MANY_CHARACTERS'))
		deplacements = [ c.deplacement for c in characters ]
		if constraint.mindeplacement != -1 and (len(deplacements) == 0 or constraint.mindeplacement > min(deplacements)): errors.append(_('CONSTRAINT_CHARACTER_TOO_SLOW'))
		if constraint.maxdeplacement != -1 and (len(deplacements) == 0 or constraint.maxdeplacement < max(deplacements)): errors.append(_('CONSTRAINT_CHARACTER_TOO_FAST'))
		if constraint.mintotaldeplacement != -1 and (len(deplacements) == 0 or constraint.mintotaldeplacement > reduce(lambda x,y: x+y, deplacements, 0)):  errors.append(_('CONSTRAINT_CHECK_NOT_ENOUGH_DEPLACEMENT'))
		if constraint.maxtotaldeplacement != -1 and (len(deplacements) == 0 or constraint.maxtotaldeplacement < reduce(lambda x,y: x+y, deplacements, 0)): errors.append(_('CONSTRAINT_CHECK_TOO_MUCH_DEPLACEMENT'))
		advdeplacements = [ c.advdeplacement() for c in characters ]
		if constraint.minadvdeplacement != -1 and (len(advdeplacements) == 0 or constraint.minadvdeplacement > min(advdeplacements)): errors.append(_('CONSTRAINT_CHARACTER_TOO_SLOWADV'))
		if constraint.maxadvdeplacement != -1 and (len(advdeplacements) == 0 or constraint.maxadvdeplacement < max(advdeplacements)): errors.append(_('CONSTRAINT_CHARACTER_TOO_FASTADV'))
		if constraint.mintotaladvdeplacement != -1 and (len(advdeplacements) == 0 or constraint.mintotaladvdeplacement > reduce(lambda x,y: x+y, advdeplacements, 0)):  errors.append(_('CONSTRAINT_CHECK_NOT_ENOUGH_DEPLACEMENTADV'))
		if constraint.maxtotaladvdeplacement != -1 and (len(advdeplacements) == 0 or constraint.maxtotaladvdeplacement < reduce(lambda x,y: x+y, advdeplacements, 0)): errors.append(_('CONSTRAINT_CHECK_TOO_MUCH_DEPLACEMENTADV'))
		forces = [ c.force for c in characters ]
		if constraint.minforce != -1 and (len(forces) == 0 or constraint.minforce > min(forces)): errors.append(_('CONSTRAINT_CHARACTER_TOO_WEAK'))
		if constraint.maxforce != -1 and (len(forces) == 0 or constraint.maxforce < max(forces)): errors.append(_('CONSTRAINT_CHARACTER_TOO_STRONG'))
		if constraint.mintotalforce != -1 and (len(forces) == 0 or constraint.mintotalforce > reduce(lambda x,y: x+y, forces, 0)):  errors.append(_('CONSTRAINT_CHECK_NOT_ENOUGH_STRENGTH'))
		if constraint.maxtotalforce != -1 and (len(forces) == 0 or constraint.maxtotalforce < reduce(lambda x,y: x+y, forces, 0)): errors.append(_('CONSTRAINT_CHECK_TOO_MUCH_STRENGH'))
		advforces = [ c.advforce () for c in characters ]
		if constraint.minadvforce != -1 and (len(advforces) == 0 or constraint.minadvforce > min(advforces)): errors.append(_('CONSTRAINT_CHARACTER_TOO_WEAKADV'))
		if constraint.maxadvforce != -1 and (len(advforces) == 0 or constraint.maxadvforce < max(advforces)): errors.append(_('CONSTRAINT_CHARACTER_TOO_STRONGADV'))
		if constraint.mintotaladvforce != -1 and (len(advforces) == 0 or constraint.mintotaladvforce > reduce(lambda x,y: x+y, advforces, 0)):  errors.append(_('CONSTRAINT_CHECK_NOT_ENOUGH_STRENGTHADV'))
		if constraint.maxtotaladvforce != -1 and (len(advforces) == 0 or constraint.maxtotaladvforce < reduce(lambda x,y: x+y, advforces, 0)): errors.append(_('CONSTRAINT_CHECK_TOO_MUCH_STRENGHADV'))
		capcount = reduce(lambda x,y: x+y, [ (1 if 'prestigious' in [ b.name for b in c.capacities() ] else 0) for c in characters ], 0)
		if constraint.minprestigious != -1 and constraint.minprestigious > capcount: errors.append(_('CONSTRAINT_NOT_ENOUGH_PRESTIGIOUS'))
		if constraint.maxprestigious != -1 and constraint.maxprestigious < capcount: errors.append(_('CONSTRAINT_CHECK_TOO_MANY_PRESTIGIOUS'))
		capcount = reduce(lambda x,y: x+y, [ (1 if 'spellcaster' in [ b.name for b in c.capacities() ] else 0) for c in characters ], 0)
		if constraint.minspellcaster != -1 and constraint.minspellcaster > capcount: errors.append(_('CONSTRAINT_NOT_ENOUGH_SPELLCASTER'))
		if constraint.maxspellcaster != -1 and constraint.maxspellcaster < capcount: errors.append(_('CONSTRAINT_CHECK_TOO_SPELLCASTERS'))
		capcount = 0
		for c in characters:
			for b in c.capacities():
				info = b.name.split('_')
				if len(info) >= 2 and info[0] == 'flyer':
					capcount += 1
		if constraint.minflying != -1 and constraint.minflying > capcount: errors.append(_('CONSTRAINT_NOT_ENOUGH_FLYING'))
		if constraint.maxflying != -1 and constraint.maxflying < capcount: errors.append(_('CONSTRAINT_CHECK_TOO_MANY_FLYING'))
		capcount = reduce(lambda x,y: x+y, [ (1 if 'immaterial' in [ b.name for b in c.capacities() ] else 0) for c in characters ], 0)
		if constraint.minintangible != -1 and constraint.minintangible > capcount: errors.append(_('CONSTRAINT_NOT_ENOUGH_IMMATERIAL'))
		if constraint.maxintangible != -1 and constraint.maxintangible < capcount: errors.append(_('CONSTRAINT_CHECK_TOO_IMMATERIAL'))
		capcount = reduce(lambda x,y: x+y, [ (1 if c.advdeplacement() >= 5 else 0) for c in characters ], 0)
		if constraint.minrunner != -1 and constraint.minrunner > capcount: errors.append(_('CONSTRAINT_NOT_ENOUGH_RUNNER'))
		if constraint.maxrunner != -1 and constraint.maxrunner < capcount: errors.append(_('CONSTRAINT_CHECK_TOO_RUNNER'))
		capcount = reduce(lambda x,y: x+y, [ (1 if c.advforce() >= 3 else 0) for c in characters ], 0)
		if constraint.minfighter != -1 and constraint.minfighter > capcount: errors.append(_('CONSTRAINT_NOT_ENOUGH_FIGHTER'))
		if constraint.maxfighter != -1 and constraint.maxfighter < capcount: errors.append(_('CONSTRAINT_CHECK_TOO_FIGHTER'))
		capcount = 0
		for c in characters:
			for b in c.capacities():
				info = b.name.split('_')
				if len(info) >= 2 and info[0] == 'walker':
					floors = info[1].split('-')
					if 'tenebres' in floors or 'tenebresmagiques' in floors:
						capcount += 1
		if constraint.minshadowwalker != -1 and constraint.minshadowwalker > capcount: errors.append(_('CONSTRAINT_NOT_ENOUGH_SHADOW_WALKER'))
		if constraint.maxshadowwalker != -1 and constraint.maxshadowwalker < capcount: errors.append(_('CONSTRAINT_CHECK_TOO_MANY_SHADOW_WALKER'))
		capcount = reduce(lambda x,y: x+y, [ (1 if 'antifountain' in [ b.name for b in c.capacities() ] else 0) for c in characters ], 0)
		if constraint.mincounterfountain != -1 and constraint.mincounterfountain > capcount: errors.append(_('CONSTRAINT_NOT_ENOUGH_COUNTERFOUNTAIN'))
		if constraint.maxcounterfountain	 != -1 and constraint.maxcounterfountain < capcount: errors.append(_('CONSTRAINT_CHECK_TOO_MANY_COUNTERFOUNTAIN'))
		mapcount = {}
		for c in characters:
			if c.name in mapcount:
				mapcount[c.name] += 1
			else:
				mapcount[c.name] = 1
		capcount = reduce(lambda x,y: x if x > y else y, mapcount.values(), 0)
		if constraint.maxsamecharacter != -1 and constraint.maxsamecharacter < capcount: errors.append(_('CONSTRAINT_TOO_MANY_IDENTICAL_CHARACTERS'))
		return errors

	@staticmethod
	def checkTeamConstraintObjets(constraintin, objects):
		errors = list()
		if type(constraintin) != DtTeamConstraint:
			constraint = DtTeamConstraint.objects.get(id=constraintin)
		else:
			constraint = constraintin
		if constraint.minobjects != -1 and constraint.minobjects > len(objects): errors.append(_('CONSTRAINT_CHECK_NOT_ENOUGH_OBJECT'))
		if constraint.maxobjects != -1 and constraint.maxobjects < len(objects): errors.append(_('CONSTRAINT_CHECK_TOO_MANY_OBJECTS'))
		capcount = reduce(lambda x,y: x+y, [ (1 if 'categorie_cursed' in [ b.name for b in c.capacities() ] else 0) for c in objects ], 0)
		if constraint.mincursed != -1 and constraint.mincursed > capcount: errors.append(_('CONSTRAINT_NOT_ENOUGH_CURSED'))
		if constraint.maxcursed != -1 and constraint.maxcursed < capcount: errors.append(_('CONSTRAINT_CHECK_TOO_MANY_CURSED'))
		capcount = reduce(lambda x,y: x+y, [ (1 if 'parchemin' in [ b.name for b in c.capacities() ] else 0) for c in objects ], 0)
		if constraint.minperchemin != -1 and constraint.minperchemin > capcount: errors.append(_('CONSTRAINT_NOT_ENOUGH_PERCHEMIN'))
		if constraint.maxperchemin != -1 and constraint.maxperchemin < capcount: errors.append(_('CONSTRAINT_CHECK_TOO_MANY_PERCHEMIN'))
		capcount = reduce(lambda x,y: x+y, [ (1 if 'categorie_arme' in [ b.name for b in c.capacities() ] else 0) for c in objects ], 0)
		if constraint.minweapon != -1 and constraint.minweapon > capcount: errors.append(_('CONSTRAINT_NOT_ENOUGH_WEAPON'))
		if constraint.maxweapon != -1 and constraint.maxweapon < capcount: errors.append(_('CONSTRAINT_CHECK_TOO_MANY_WEAPON'))
		mapcount = {}
		for c in objects:
			if 'categorie_current' not in [ cap.name for cap in c.capacities() ]:
				if c.name in mapcount:
					mapcount[c.name] += 1
				else:
					mapcount[c.name] = 1
		capcount = reduce(lambda x,y: x if x > y else y, mapcount.values(), 0)
		if constraint.maxsameobject != -1 and constraint.maxsameobject < capcount: errors.append(_('CONSTRAINT_TOO_MANY_SAME_OBJECTS'))
		mapcount = {}
		for c in objects:
			if 'categorie_current' in [ cap.name for cap in c.capacities() ]:
				if c.name in mapcount:
					mapcount[c.name] += 1
				else:
					mapcount[c.name] = 1
		capcount = reduce(lambda x,y: x if x > y else y, mapcount.values(), 0)
		if constraint.maxcommonobject != -1 and constraint.maxcommonobject < capcount: errors.append(_('CONSTRAINT_TOO_MANY_COMMON_OBJETS'))
		return errors
		
	@staticmethod
	def checkTeamConstraintRooms(constraintin, roomsin):
		errors = list()
		if type(constraintin) != DtTeamConstraint:
			constraint = DtTeamConstraint.objects.get(id=constraintin)
		else:
			constraint = constraintin
		rooms = list()
		for c in roomsin:
			if isinstance(c, (list, tuple)):
				rooms.append(c[0])
				rooms.append(c[1])
			else:
				rooms.append(c)
		if constraint.minrooms != -1 and constraint.minrooms > len(rooms)/2: errors.append(_('CONSTRAINT_CHECK_NOT_ENOUGH_ROOM'))
		if constraint.maxrooms != -1 and constraint.maxrooms < len(rooms)/2: errors.append(_('CONSTRAINT_CHECK_TOO_MANY_ROOMS'))
		capcount = reduce(lambda x,y: x+y, [ (1 if 'tenebres' in [ b.name for b in c.categories.all() ] else 0) for c in rooms ], 0)
		if constraint.minshadowroom != -1 and constraint.minshadowroom > capcount: errors.append(_('CONSTRAINT_NOT_ENOUGH_SHADOW_ROOMS'))
		if constraint.maxshadowroom	!= -1 and constraint.maxshadowroom < capcount: errors.append(_('CONSTRAINT_CHECK_TOO_MANY_SHADOW_ROOMS'))
		capcount = reduce(lambda x,y: x+y, [ (1 if 'antimagie' in [ b.name for b in c.categories.all() ] else 0) for c in rooms ], 0)
		if constraint.minantimagicroom != -1 and constraint.minantimagicroom > capcount: errors.append(_('CONSTRAINT_NOT_ENOUGH_ANTIMAGIC_ROOMS'))
		if constraint.maxantimagicroom	 != -1 and constraint.maxantimagicroom < capcount: errors.append(_('CONSTRAINT_CHECK_TOO_ANTIMAGIC_ROOMS'))
		capcount = reduce(lambda x,y: x+y, [ (1 if 'fontaine' in [ b.name for b in c.categories.all() ] else 0) for c in rooms ], 0)
		if constraint.minfountain != -1 and constraint.minfountain > capcount: errors.append(_('CONSTRAINT_NOT_ENOUGH_FOUNTAINS'))
		if constraint.maxfountain	 != -1 and constraint.maxfountain < capcount: errors.append(_('CONSTRAINT_CHECK_TOO_MANY_FOUNTAINS'))
		mapcount = {}
		for c in rooms:
			if c.rotation == 1:
				if c.number in mapcount:
					mapcount[c.number] += 1
				else:
					mapcount[c.number] = 1
		capcount = reduce(lambda x,y: x if x > y else y, mapcount.values(), 0)
		if constraint.maxsameroom != -1 and constraint.maxsameroom < capcount: errors.append(_('CONSTRAINT_TOO_MANY_IDENTICAL_ROOMS'))
		return errors

	def checkTeamConstraint(self, constraintin, characters, objects, rooms):
		errors = list()
		if type(constraintin) != DtTeamConstraint:
			constraint = DtTeamConstraint.objects.get(id=constraintin)
		else:
			constraint = constraintin
		errors += TeamManager.checkTeamConstraintCharacters(constraintin, characters)
		errors += TeamManager.checkTeamConstraintObjects(constraintin, objects)
		errors += TeamManager.checkTeamConstraintRooms(constraintin, rooms)
		extensionslistlist = [ [] ]
		for c in characters:
			nl = list()
			found = False
			for e in c.extensions.all():
				for extensionslist in extensionslistlist:
					if e.name not in extensionslist:
						nl.append(extensionslist+[e.name])
					else:
						found = True
			if not found:
				extensionslistlist = nl
		for c in objects:
			nl = list()
			found = False
			for e in c.extensions.all():
				for extensionslist in extensionslistlist:
					if e.name not in extensionslist:
						nl.append(extensionslist+[e.name])
					else:
						found = True
			if not found:
				extensionslistlist = nl
		for c in rooms:
			nl = list()
			found = False
			for e in c.extensions.all():
				for extensionslist in extensionslistlist:
					if e.name not in extensionslist:
						nl.append(extensionslist+[e.name])
					else:
						found = True
			if not found:
				extensionslistlist = nl
		extensionslistlist = [ set(e) for e in extensionslistlist ]
		capcount = reduce(lambda x,y: x if x < y else y, [ len(ell) for ell in extensionslistlist])
		if constraint.minextensions != -1 and constraint.minextensions > capcount: errors.append(_('CONSTRAINT_NOT_ENOUGH_EXTENSIONS'))
		if constraint.maxextensions != -1 and constraint.maxextensions < capcount: errors.append(_('CONSTRAINT_CHECK_TOO_MANY_EXTENSIONS'))
		extensions = set([ e.name for e in constraint.extensions.all() ])
		if len(extensions) > 0:
			found = False
			for extensionslist in extensionslistlist:
				if len(extensions.intersection(extensionslist)) == len(extensionslist):
					found = True
					break
			if not found: errors.append(_('CONSTRAINT_FORBIDEN_EXTENSION_%s') % ', '.join([ _('EXTENSION_%s' % (n)) for n in extensions ]))
		return errors

	def generateRandomTeam(self, method, teamscount, tc, repeat):
		maxtries = 100
		teams = list()
		extensions = self.extensionManager.getExtensions(tc.extensions)
		extsid = [ e.id for e in extensions ]
		characterscount = tc.maxcharacters
		objectscount = tc.maxobjects
		roomscount = tc.maxrooms
		characterslist = [ c for c in self.spawnManager.getCharacters(extensions) ]
		objectslist = self.spawnManager.getObjects(extensions)
		objscount = len(objectslist)
		objscurrent = set()
		for o in objectslist:
			toadd = 0
			for cap in o.capacities():
				if cap.name == u'categorie_current':
					objscurrent.add(o.name)
					for ext in o.extensions.all():
						if ext.id in extsid:
							objscount += toadd
							toadd = 1
					break
		roomslistraw = self.spawnManager.getRooms(extensions)
		roomsmap = dict()
		for r in roomslistraw:
			if r.number not in roomsmap:
				roomsmap[r.number] = ()
			roomsmap[r.number] += (r,)
		roomslist = roomsmap.values()
		if len(characterslist) < characterscount*(1 if repeat else teamscount):
			raise Exception(_('RANDOMTEAM_NOT_ENOUGH_CHARACTERS'))
		if objscount < objectscount*(1 if repeat else teamscount):
			raise Exception(_('RANDOMTEAM_NOT_ENOUGH_OBJECTS'))
		if len(roomslist) < roomscount*(1 if repeat else teamscount):
			raise Exception(_('RANDOMTEAM_NOT_ENOUGH_ROOMS'))
		charactersfilters = set()
		objectsfilters = set()
		roomsfilters = set()
		for i in range(0, teamscount):
			if method == 'random':
				characters = self._generateRandom(characterslist, lambda x: x.name, tc, TeamManager.filterConstraintCharacters, TeamManager.checkTeamConstraintCharacters, characterscount, maxtries)
				objects = self._generateRandom(objectslist, lambda x: x.name, tc, TeamManager.filterConstraintObjects, TeamManager.checkTeamConstraintObjets, objectscount, maxtries)
				rooms = self._generateRandom(roomslist, lambda x: x[0].number, tc, TeamManager.filterConstraintRooms, TeamManager.checkTeamConstraintRooms, roomscount, maxtries)
			elif method == '3221':
				characters = self._generate3221(characterslist, tc, TeamManager.filterConstraintCharacters, TeamManager.checkTeamConstraintCharacters, characterscount)
				objects = self._generateRandom(objectslist, lambda x: x.name, tc, TeamManager.filterConstraintObjects, TeamManager.checkTeamConstraintObjets, objectscount, maxtries)
				rooms = self._generateRandom(roomslist, lambda x: x[0].number, tc, TeamManager.filterConstraintRooms, TeamManager.checkTeamConstraintRooms, roomscount, maxtries)
			elif method == 'clever':
				rooms = self._generateRandom(roomslist, lambda x: x[0].number, tc, TeamManager.filterConstraintRooms, TeamManager.checkTeamConstraintRooms, roomscount, maxtries)
				characters = self._generateCleverCharacters(characterslist, tc, TeamManager.filterConstraintCharacters, TeamManager.checkTeamConstraintCharacters, characterscount, rooms)
				objects = self._generateCleverObjects(objectslist, objectsfilters, tc, TeamManager.filterConstraintObjects, TeamManager.checkTeamConstraintObjets, objectscount, rooms, characters)
			teams.append((characters, objects, rooms))
			if not repeat:
				characterslist -= characters
				objectslist -= objects
				roomslist -= rooms
		return teams

	@staticmethod
	def filterConstraintCharacters(tc, characterslist, characters):
		''' Modify charcterslist, objectslist, roomslist according to characters, objets and rooms already taken '''
		if len(characters) >= tc.maxcharacters:
			characterslist[:] = []
			return

		capcountintangible = reduce(lambda x,y: x+y, [ (1 if 'immaterial' in [ b.name for b in c.capacities() ] else 0) for c in characters ], 0)
		capcountcounterfountain = reduce(lambda x,y: x+y, [ (1 if 'antifountain' in [ b.name for b in c.capacities() ] else 0) for c in characters ], 0)
		capcountprestigious = reduce(lambda x,y: x+y, [ (1 if 'prestigious' in [ b.name for b in c.capacities() ] else 0) for c in characters ], 0)
		capcountspellcaster = reduce(lambda x,y: x+y, [ (1 if 'spellcaster' in [ b.name for b in c.capacities() ] else 0) for c in characters ], 0)
		capcountrunner = reduce(lambda x,y: x+y, [ (1 if c.advdeplacement() >= 5 else 0) for c in characters ], 0)
		capcountfighter = reduce(lambda x,y: x+y, [ (1 if c.advforce() >= 3 else 0) for c in characters ], 0)
		capcountshadowwalker = 0
		for c in characters:
			for b in c.capacities():
				info = b.name.split('_')
				if len(info) >= 2 and info[0] == 'walker':
					floors = info[1].split('-')
					if 'tenebres' in floors or 'tenebresmagiques' in floors:
						capcountshadowwalker += 1
		capcountflyer = 0
		for c in characters:
			for b in c.capacities():
				info = b.name.split('_')
				if len(info) >= 2 and info[0] == 'flyer':
					capcountflyer += 1

		characterslistf = None
		if tc.minrunner != -1 and capcountrunner < tc.minrunner:
			if characterslistf is None: characterslistf = set()
			for idx in xrange(len(characterslist)-1, -1, -1):
				if characterslist[idx].advdeplacement() >= 5: characterslistf.add(characterslist[idx])
		if tc.minfighter != -1 and capcountfighter < tc.minfighter:
			if characterslistf is None: characterslistf = set()
			for idx in xrange(len(characterslist)-1, -1, -1):
				if characterslist[idx].advforce() >= 3: characterslistf.add(characterslist[idx])
		if tc.minintangible != -1 and capcountintangible < tc.minintangible:
			if characterslistf is None: characterslistf = set()
			for idx in xrange(len(characterslist)-1, -1, -1):
				if 'immaterial' in [ b.name for b in characterslist[idx].capacities() ]: characterslistf.add(characterslist[idx])
		if tc.mincounterfountain != -1 and capcountcounterfountain < tc.mincounterfountain:
			if characterslistf is None: characterslistf = set()
			for idx in xrange(len(characterslist)-1, -1, -1):
				if 'antifountain' in [ b.name for b in characterslist[idx].capacities() ]: characterslistf.add(characterslist[idx])
		if tc.minspellcaster != -1 and capcountspellcaster < tc.minspellcaster:
			if characterslistf is None: characterslistf = set()
			for idx in xrange(len(characterslist)-1, -1, -1):
				if 'spellcaster' in [ b.name for b in characterslist[idx].capacities() ]: characterslistf.add(characterslist[idx])
		if tc.minprestigious != -1 and capcountprestigious < tc.minprestigious:
			if characterslistf is None: characterslistf = set()
			for idx in xrange(len(characterslist)-1, -1, -1):
				if 'prestigious' in [ b.name for b in characterslist[idx].capacities() ]: characterslistf.add(characterslist[idx])
		if tc.minflying != -1 and capcountflyer < tc.minflying:
			if characterslistf is None: characterslistf = set()
			for idx in xrange(len(characterslist)-1, -1, -1):
				for b in characterslist[idx].capacities():
					info = b.name.split('_')
					if len(info) >= 2 and info[0] == 'flyer':
						characterslistf.add(characterslist[idx])
		if tc.minshadowwalker != -1 and capcountshadowwalker < tc.minshadowwalker:
			if characterslistf is None: characterslistf = set()
			for idx in xrange(len(characterslist)-1, -1, -1):
				for b in characterslist[idx].capacities():
					info = b.name.split('_')
					if len(info) >= 2 and info[0] == 'walker':
						floors = info[1].split('-')
						if 'tenebres' in floors or 'tenebresmagiques' in floors:
							characterslistf.add(characterslist[idx])
		if characterslistf is not None: characterslist[:] = characterslistf
		
		if tc.mindeplacement != -1:
			for idx in xrange(len(characterslist)-1, -1, -1):
				if characterslist[idx].deplacement < tc.mindeplacement: del characterslist[idx]
		if tc.maxdeplacement != -1:
			for idx in xrange(len(characterslist)-1, -1, -1):
				if characterslist[idx].deplacement > tc.maxdeplacement: del characterslist[idx]
		if tc.minadvdeplacement != -1:
			for idx in xrange(len(characterslist)-1, -1, -1):
				if characterslist[idx].advdeplacement() < tc.minadvdeplacement: del characterslist[idx]
		if tc.maxadvdeplacement != -1:
			for idx in xrange(len(characterslist)-1, -1, -1):
				if characterslist[idx].advdeplacement() > tc.maxadvdeplacement: del characterslist[idx]
		if tc.minforce != -1:
			for idx in xrange(len(characterslist)-1, -1, -1):
				if characterslist[idx].force < tc.minforce: del characterslist[idx]
		if tc.maxforce != -1:
			for idx in xrange(len(characterslist)-1, -1, -1):
				if characterslist[idx].force > tc.maxforce:
					del characterslist[idx]
		if tc.minadvforce != -1:
			for idx in xrange(len(characterslist)-1, -1, -1):
				if characterslist[idx].advforce() < tc.minadvforce: del characterslist[idx]
		if tc.maxadvforce != -1:
			for idx in xrange(len(characterslist)-1, -1, -1):
				if characterslist[idx].advforce() > tc.maxadvforce: del characterslist[idx]
		if tc.maxprestigious != -1 and capcountprestigious >= tc.maxprestigious:
			for idx in xrange(len(characterslist)-1, -1, -1):
				if 'prestigious' in [ b.name for b in characterslist[idx].capacities() ]: del characterslist[idx]
		if tc.maxspellcaster != -1 and capcountspellcaster >= tc.maxspellcaster:
			for idx in xrange(len(characterslist)-1, -1, -1):
				if 'spellcaster' in [ b.name for b in characterslist[idx].capacities() ]: del characterslist[idx]
		if tc.maxflying != -1 and capcountflyer >= tc.maxflying:
			for idx in xrange(len(characterslist)-1, -1, -1):
				for b in characterslist[idx].capacities():
					info = b.name.split('_')
					if len(info) >= 2 and info[0] == 'flyer':
						del characterslist[idx]
		if tc.maxintangible != -1 and capcountintangible >= tc.maxintangible:
			for idx in xrange(len(characterslist)-1, -1, -1):
				if 'immaterial' in [ b.name for b in characterslist[idx].capacities() ]: del characterslist[idx]
		if tc.maxrunner != -1 and capcountrunner >= tc.maxrunner:
			for idx in xrange(len(characterslist)-1, -1, -1):
				if characterslist[idx].advdeplacement() >= 5: del characterslist[idx]
		if tc.maxfighter != -1 and capcountfighter >= tc.maxfighter:
			for idx in xrange(len(characterslist)-1, -1, -1):
				if characterslist[idx].advforce() >= 3: del characterslist[idx]
		if tc.maxshadowwalker != -1 and capcountshadowwalker >= tc.maxshadowwalker:
			for idx in xrange(len(characterslist)-1, -1, -1):
				for b in characterslist[idx].capacities():
					info = b.name.split('_')
					if len(info) >= 2 and info[0] == 'walker':
						floors = info[1].split('-')
						if 'tenebres' in floors or 'tenebresmagiques' in floors:
							del characterslist[idx]
		if tc.maxcounterfountain != -1 and capcountcounterfountain >= tc.maxcounterfountain:
			for idx in xrange(len(characterslist)-1, -1, -1):
				if 'antifountain' in [ b.name for b in characterslist[idx].capacities() ]: del characterslist[idx]
		if tc.maxsamecharacter != -1:
			for idx in xrange(len(characterslist)-1, -1, -1):
				if characterslist[idx] in characters:
					count = 0
					for c in characters:
						if c.name == characterslist[idx].name: count += 1
					if count >= tc.maxsamecharacter:
						del characterslist[idx]

	@staticmethod
	def filterConstraintObjects(tc, objectslist, objects):
		if len(objects) >= tc.maxobjects:
			objectslist[:] = []
			return

		capcountcursed = reduce(lambda x,y: x+y, [ (1 if 'categorie_cursed' in [ b.name for b in c.capacities() ] else 0) for c in objects ], 0)
		capcountperchemin = reduce(lambda x,y: x+y, [ (1 if 'parchemin' in [ b.name for b in c.capacities() ] else 0) for c in objects ], 0)
		capcountarme = reduce(lambda x,y: x+y, [ (1 if 'categorie_arme' in [ b.name for b in c.capacities() ] else 0) for c in objects ], 0)

		objectslistf = None
		if tc.mincursed != -1 and capcountcursed < tc.mincursed:
			if objectslistf is None: objectslistf = set()
			for idx in xrange(len(objectslist)-1, -1, -1):
				if 'categorie_cursed' in [ b.name for b in objectslist[idx].capacities() ]: objectslistf.add(objectslist[idx])
		if tc.minperchemin != -1 and capcountperchemin < tc.minperchemin:
			if objectslistf is None: objectslistf = set()
			for idx in xrange(len(objectslist)-1, -1, -1):
				if 'parchemin' in [ b.name for b in objectslist[idx].capacities() ]: objectslistf.add(objectslist[idx])
		if tc.minweapon != -1 and capcountarme < tc.minweapon:
			if objectslistf is None: objectslistf = set()
			for idx in xrange(len(objectslist)-1, -1, -1):
				if 'categorie_arme' in [ b.name for b in objectslist[idx].capacities() ]: objectslistf.add(objectslist[idx])
		if objectslistf is not None: objectslist[:] = objectslistf

		if tc.maxcursed != -1 and capcountcursed >= tc.maxcursed:
			for idx in xrange(len(objectslist)-1, -1, -1):
				if 'categorie_cursed' in [ b.name for b in objectslist[idx].capacities() ]: del objectslist[idx]
		if tc.maxperchemin != -1 and capcountperchemin >= tc.maxperchemin:
			for idx in xrange(len(objectslist)-1, -1, -1):
				if 'parchemin' in [ b.name for b in objectslist[idx].capacities() ]: del objectslist[idx]
		if tc.maxweapon != -1 and capcountarme >= tc.maxweapon:
			for idx in xrange(len(objectslist)-1, -1, -1):
				if 'categorie_arme' in [ b.name for b in objectslist[idx].capacities() ]: del objectslist[idx]

		if tc.maxcommonobject != -1:
			for idx in xrange(len(objectslist)-1, -1, -1):
				if objectslist[idx] in objects and 'categorie_current' in [ cap.name for cap in objectslist[idx].capacities() ]:
					count = 0
					for c in objects:
						if c.name == objectslist[idx].name: count += 1
					if count >= tc.maxcommonobject:
						del objectslist[idx]
		if tc.maxsameobject != -1:
			for idx in xrange(len(objectslist)-1, -1, -1):
				if objectslist[idx] in objects and 'categorie_current' not in [ cap.name for cap in objectslist[idx].capacities() ]:
					count = 0
					for c in objects:
						if c.name == objectslist[idx].name: count += 1
					if count >= tc.maxsameobject:
						del objectslist[idx]


	@staticmethod
	def filterConstraintRooms(tc, roomslist, rooms):
		if len(rooms) >= tc.maxrooms:
			roomslist[:] = []
			return

		capcounttenebres = reduce(lambda x,y: x+y, [ (1 if 'tenebres' in [b.name for b in c[0].categories.all()] else 0) + (1 if 'tenebres' in [b.name for b in c[1].categories.all()] else 0) for c in rooms ], 0)
		capcountantimagie = reduce(lambda x,y: x+y, [ (1 if 'antimagie' in [b.name for b in c[0].categories.all()] else 0) + (1 if 'antimagie' in [b.name for b in c[1].categories.all()] else 0) for c in rooms ], 0)
		capcountfontaine = reduce(lambda x,y: x+y, [ (1 if 'fontaine' in [b.name for b in c[0].categories.all()] else 0) + (1 if 'fontaine' in [b.name for b in c[1].categories.all()] else 0) for c in rooms ], 0)

		roomslistf = None
		if tc.minshadowroom != -1 and capcounttenebres < tc.minshadowroom:
			if roomslistf is None: roomslistf = set()
			for idx in xrange(len(roomslist)-1, -1, -1):
				if 'tenebres' in [b.name for b in roomslist[idx][0].categories.all()] or 'tenebres' in [b.name for b in roomslist[idx][1].categories.all()]: roomslistf.add(roomslist[idx])
		if tc.minfountain != -1 and capcountfontaine < tc.minfountain:
			if roomslistf is None: roomslistf = set()
			for idx in xrange(len(roomslist)-1, -1, -1):
				if 'fontaine' in [b.name for b in roomslist[idx][0].categories.all()]+[b.name for b in roomslist[idx][1].categories.all()]: roomslistf.add(roomslist[idx])
		if tc.minantimagicroom != -1 and capcountantimagie < tc.minantimagicroom:
			if roomslistf is None: roomslistf = set()
			for idx in xrange(len(roomslist)-1, -1, -1):
				if 'antimagie' in [b.name for b in roomslist[idx][0].categories.all()]+[b.name for b in roomslist[idx][1].categories.all()]: roomslistf.add(roomslist[idx])
		if roomslistf is not None: roomslist[:] = roomslistf

		if tc.maxfountain != -1 and capcountfontaine >= tc.maxfountain:
			for idx in xrange(len(roomslist)-1, -1, -1):
				if 'fontaine' in [b.name for b in roomslist[idx][0].categories.all()]+[b.name for b in roomslist[idx][1].categories.all()]: del roomslist[idx]
		if tc.maxantimagicroom != -1 and capcountantimagie >= tc.maxantimagicroommaxfountain:
			for idx in xrange(len(roomslist)-1, -1, -1):
				if 'antimagie' in [b.name for b in roomslist[idx][0].categories.all()]+[b.name for b in roomslist[idx][1].categories.all()]: del roomslist[idx]
		if tc.maxshadowroom != -1 and capcounttenebres >= tc.maxshadowroom:
			for idx in xrange(len(roomslist)-1, -1, -1):
				if 'tenebres' in [b.name for b in roomslist[idx][0].categories.all()]+[b.name for b in roomslist[idx][1].categories.all()]: del roomslist[idx]
		print tc.minshadowroom, capcounttenebres, roomslist
			
		if tc.maxsameroom != -1:
			for idx in xrange(len(roomslist)-1, -1, -1):
				if roomslist[idx] in rooms:
					count = 0
					for c in rooms:
						if c == roomslist[idx]: count += 1
					if count >= tc.maxsameroom:
						del roomslist[idx]


	def _generateRandom(self, arraysrci, key, tc, filtermethod, checkmethod, count, maxtries):
		''' generate from src using key (to get unique) and not in filters (filters is a set) '''
		notdone = True
		tries = 0
		while notdone:
			array = list()
			while len(array) < count:
				arraysrc = arraysrci[:]
				filtermethod(tc, arraysrc, array)
				if len(arraysrc) == 0:
					raise Exception("NO_ENOUGH")
				c = random.choice(arraysrc)
				k = key(c)
				array.append(c)
			errors = checkmethod(tc, array)
			notdone = len(errors) != 0
			tries += 1
			if tries >= maxtries: raise Exception("UNABLE_TO_GENERATE_RANDOM")
		return array
	
	def _generate3221(self, arraysrc, tc, count):
		''' generate from src using key (to get unique) and not in filters (filters is a set) '''
		array = list()
		categslimit = [ int(math.ceil(3*8.0/count)), int(math.ceil(2*8.0/count)), int(math.ceil(2*8.0/count)), int(math.ceil(1*8.0/count)) ]
		categs = [ [], [], [], [] ]
		for c in arraysrc:
			if c.name not in filters:
				if c.force <= 1: categs[0].append(c)
				elif c.force == 2: categs[1].append(c)
				elif c.force == 3: categs[2].append(c)
				else: categs[3].append(c)
		for i in range(0, len(categs)):
			if len(categs[i]) < categslimit[i]:
				raise Exception(_('RANDOMTEAM_NOT_ENOUGH_CHARACTERS'))
			array.extend(self._generateRandom(categs[i], lambda x: x.name, tc, TeamManager.filterConstraintCharacters, categslimit[i]))
		return array
	
	def _generateCleverCharacters(self, characterslist, charactersfilters, characterscount, rooms):
		# si ténèbres => biendans_tenebres requis sinon interdit
		# si lave => biendans_feu requis sinon interdit
		# si arbre => biendans_arbre sinon interdit
		# si eau => biendans_eau et supprime craint_eau sinon interdit biendans_eau
		# si neige => biendans_neige
		# si meurtriere => biendans_meurtriere sinon interdit
		# si pentes => biendans_pente sinon interdit
		# si rocher => biendans_rocher sinon interdit
		# si fontaine => biendans_fontaine sinon interdit
		# si torche => pas de dissout dans la lumière (sauf si torche+ténèbres)
		# si vermine => biendans_vermine sinon interdit
		# Voir quelles sont les capacitées requises et interdites
		# sélectionner les personnages aléatoirement en ayant pré filtré
		pass

	def _generateCleverObjects(self, objectslist, objectsfilters, objscurrent, objectscount, rooms, characters):
		pass

	
