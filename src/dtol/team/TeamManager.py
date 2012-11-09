# -*- coding: utf-8 -*-
#
# This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
#

from dtol.models import DtTeam, DtTeamConstraint, DtCharacter
from django.utils.translation import ugettext as _

class TeamManager(object):
	'''
	Manage user, authentication and data
	'''

	def getTeams(self, user):
		return DtTeam.objects.filter(user=user.id)

	def getTeamConstraints(self, protected=None, game=None):
		kwargs = { 'deleted': 0 }
		if protected is not None:
			kwargs['protected'] = protected
		kwargs['game'] = game
		return DtTeamConstraint.objects.filter(**kwargs)

	def delTeamConstraint(self, uid):
		DtTeamConstraint.objects.filter(id=uid).update(deleted=1)

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
			if 'current' in capacities: sp['filters'].append('current')
			if 'magical' in capacities: sp['filters'].append('magical')
			if 'parchemin' in capacities: sp['filters'].append('parchemin')
			if 'categorie_arme' in capacities: sp['filters'].append('categorie_arme')
			if 'shield' in capacities: sp['filters'].append('shield')
			if 'categorie_puissant' in capacities: sp['filters'].append('categorie_puissant')
			if 'antifountain' in capacities: sp['filters'].append('antifountain')
			if 'cursed' in capacities: sp['filters'].append('cursed')
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

	def checkTeamConstraint(self, constraintin, characters, objects, rooms):
		errors = list()
		if type(constraintin) != DtTeamConstraint:
			constraint = DtTeamConstraint.objects.get(id=constraintin)
		else:
			constraint = constraintin
		if constraint.mincharacters != -1 and constraint.mincharacters > len(characters): errors.append(_('CONSTRAINT_CHECK_NOT_ENOUGH_CHARACTER'))
		if constraint.maxcharacters != -1 and constraint.maxcharacters < len(characters): errors.append(_('CONSTRAINT_CHECK_TOO_MANY_CHARACTERS'))
		if constraint.minobjects != -1 and constraint.minobjects > len(objects): errors.append(_('CONSTRAINT_CHECK_NOT_ENOUGH_OBJECT'))
		if constraint.maxobjects != -1 and constraint.maxobjects < len(objects): errors.append(_('CONSTRAINT_CHECK_TOO_MANY_OBJECTS'))
		if constraint.minrooms != -1 and constraint.minrooms > len(rooms)/2: errors.append(_('CONSTRAINT_CHECK_NOT_ENOUGH_ROOM'))
		if constraint.maxrooms != -1 and constraint.maxrooms < len(rooms)/2: errors.append(_('CONSTRAINT_CHECK_TOO_MANY_ROOMS'))
		deplacements = [ c.deplacement for c in characters ]
		if constraint.mindeplacement != -1 and (len(deplacements) == 0 or constraint.mindeplacement > min(deplacements)): errors.append(_('CONSTRAINT_CHARACTER_TOO_SLOW'))
		if constraint.maxdeplacement != -1 and (len(deplacements) == 0 or constraint.maxdeplacement < max(deplacements)): errors.append(_('CONSTRAINT_CHARACTER_TOO_FAST'))
		if constraint.mintotaldeplacement != -1 and (len(deplacements) == 0 or constraint.mintotaldeplacement > reduce(lambda x,y: x+y, deplacements)):  errors.append(_('CONSTRAINT_CHECK_NOT_ENOUGH_DEPLACEMENT'))
		if constraint.maxtotaldeplacement != -1 and (len(deplacements) == 0 or constraint.maxtotaldeplacement < reduce(lambda x,y: x+y, deplacements)): errors.append(_('CONSTRAINT_CHECK_TOO_MUCH_DEPLACEMENT'))
		advdeplacements = [ c.advdeplacement() for c in characters ]
		if constraint.minadvdeplacement != -1 and (len(advdeplacements) == 0 or constraint.minadvdeplacement > min(advdeplacements)): errors.append(_('CONSTRAINT_CHARACTER_TOO_SLOW'))
		if constraint.maxadvdeplacement != -1 and (len(advdeplacements) == 0 or constraint.maxadvdeplacement < max(advdeplacements)): errors.append(_('CONSTRAINT_CHARACTER_TOO_FAST'))
		if constraint.mintotaladvdeplacement != -1 and (len(advdeplacements) == 0 or constraint.mintotaladvdeplacement > reduce(lambda x,y: x+y, advdeplacements)):  errors.append(_('CONSTRAINT_CHECK_NOT_ENOUGH_DEPLACEMENT'))
		if constraint.maxtotaladvdeplacement != -1 and (len(advdeplacements) == 0 or constraint.maxtotaladvdeplacement < reduce(lambda x,y: x+y, advdeplacements)): errors.append(_('CONSTRAINT_CHECK_TOO_MUCH_DEPLACEMENT'))
		forces = [ c.force for c in characters ]
		if constraint.minforce != -1 and (len(forces) == 0 or constraint.minforce > min(forces)): errors.append(_('CONSTRAINT_CHARACTER_TOO_WEAK'))
		if constraint.maxforce != -1 and (len(forces) == 0 or constraint.maxforce < max(forces)): errors.append(_('CONSTRAINT_CHARACTER_TOO_STRONG'))
		if constraint.mintotalforce != -1 and (len(forces) == 0 or constraint.mintotalforce > reduce(lambda x,y: x+y, forces)):  errors.append(_('CONSTRAINT_CHECK_NOT_ENOUGH_STRENGTH'))
		if constraint.maxtotalforce != -1 and (len(forces) == 0 or constraint.maxtotalforce < reduce(lambda x,y: x+y, forces)): errors.append(_('CONSTRAINT_CHECK_TOO_MUCH_STRENGH'))
		advforces = [ c.advforce () for c in characters ]
		if constraint.minadvforce != -1 and (len(advforces) == 0 or constraint.minadvforce > min(advforces)): errors.append(_('CONSTRAINT_CHARACTER_TOO_WEAK'))
		if constraint.maxadvforce != -1 and (len(advforces) == 0 or constraint.maxadvforce < max(advforces)): errors.append(_('CONSTRAINT_CHARACTER_TOO_STRONG'))
		if constraint.mintotaladvforce != -1 and (len(advforces) == 0 or constraint.mintotaladvforce > reduce(lambda x,y: x+y, advforces)):  errors.append(_('CONSTRAINT_CHECK_NOT_ENOUGH_STRENGTH'))
		if constraint.maxtotaladvforce != -1 and (len(advforces) == 0 or constraint.maxtotaladvforce < reduce(lambda x,y: x+y, advforces)): errors.append(_('CONSTRAINT_CHECK_TOO_MUCH_STRENGH'))
		capcount = reduce(lambda x,y: x+y, [ (1 if 'prestigious' in [ b.name for b in c.capacities() ] else 0) for c in characters ])
		if constraint.minprestigious != -1 and constraint.minprestigious > capcount: errors.append(_('CONSTRAINT_NOT_ENOUGH_PRESTIGIOUS'))
		if constraint.maxprestigious != -1 and constraint.maxprestigious < capcount: errors.append(_('CONSTRAINT_CHECK_TOO_MANY_PRESTIGIOUS'))
		capcount = reduce(lambda x,y: x+y, [ (1 if 'prestigious' in [ b.name for b in c.capacities() ] else 0) for c in characters ])
		if constraint.minspellcaster != -1 and constraint.minspellcaster : errors.append(_('CONSTRAINT_CHECK_TOO_MANY_CHARACTERS'))
		if constraint.maxspellcaster != -1 and constraint.maxspellcaster : errors.append(_('CONSTRAINT_CHECK_TOO_MANY_CHARACTERS'))
		capcount = reduce(lambda x,y: x+y, [ (1 if 'prestigious' in [ b.name for b in c.capacities() ] else 0) for c in characters ])
		if constraint.minflying != -1 and constraint.minflying : errors.append(_('CONSTRAINT_CHECK_TOO_MANY_CHARACTERS'))
		if constraint.maxflying != -1 and constraint.maxflying : errors.append(_('CONSTRAINT_CHECK_TOO_MANY_CHARACTERS'))
		capcount = reduce(lambda x,y: x+y, [ (1 if 'prestigious' in [ b.name for b in c.capacities() ] else 0) for c in characters ])
		if constraint.minintangible != -1 and constraint.minintangible : errors.append(_('CONSTRAINT_CHECK_TOO_MANY_CHARACTERS'))
		if constraint.maxintangible != -1 and constraint.maxintangible : errors.append(_('CONSTRAINT_CHECK_TOO_MANY_CHARACTERS'))
		capcount = reduce(lambda x,y: x+y, [ (1 if 'prestigious' in [ b.name for b in c.capacities() ] else 0) for c in characters ])
		if constraint.mincursed != -1 and constraint.mincursed : errors.append(_('CONSTRAINT_CHECK_TOO_MANY_CHARACTERS'))
		if constraint.maxcursed != -1 and constraint.maxcursed : errors.append(_('CONSTRAINT_CHECK_TOO_MANY_CHARACTERS'))
		if constraint.minshadowwalker != -1 and constraint.minshadowwalker : errors.append(_('CONSTRAINT_CHECK_TOO_MANY_CHARACTERS'))
		if constraint.maxshadowwalker != -1 and constraint.maxshadowwalker : errors.append(_('CONSTRAINT_CHECK_TOO_MANY_CHARACTERS'))
		if constraint.minshadowroom != -1 and constraint.minshadowroom : errors.append(_('CONSTRAINT_CHECK_TOO_MANY_CHARACTERS'))
		if constraint.maxshadowroom	 != -1 and constraint.maxshadowroom	 : errors.append(_('CONSTRAINT_CHECK_TOO_MANY_CHARACTERS'))
		if constraint.minantimagicroom != -1 and constraint.minantimagicroom : errors.append(_('CONSTRAINT_CHECK_TOO_MANY_CHARACTERS'))
		if constraint.maxantimagicroom	 != -1 and constraint.maxantimagicroom	 : errors.append(_('CONSTRAINT_CHECK_TOO_MANY_CHARACTERS'))
		if constraint.minfountain != -1 and constraint.minfountain : errors.append(_('CONSTRAINT_CHECK_TOO_MANY_CHARACTERS'))
		if constraint.maxfountain	 != -1 and constraint.maxfountain	 : errors.append(_('CONSTRAINT_CHECK_TOO_MANY_CHARACTERS'))
		if constraint.mincounterfountain != -1 and constraint.mincounterfountain : errors.append(_('CONSTRAINT_CHECK_TOO_MANY_CHARACTERS'))
		if constraint.maxcounterfountain	 != -1 and constraint.maxcounterfountain	 : errors.append(_('CONSTRAINT_CHECK_TOO_MANY_CHARACTERS'))
		if constraint.minextensions != -1 and constraint.minextensions : errors.append(_('CONSTRAINT_CHECK_TOO_MANY_CHARACTERS'))
		if constraint.maxextensions != -1 and constraint.maxextensions : errors.append(_('CONSTRAINT_CHECK_TOO_MANY_CHARACTERS'))
		if constraint.maxsamecharacter != -1 and constraint.maxsamecharacter : errors.append(_('CONSTRAINT_CHECK_TOO_MANY_CHARACTERS'))
		if constraint.maxsameobject != -1 and constraint.maxsameobject : errors.append(_('CONSTRAINT_CHECK_TOO_MANY_CHARACTERS'))
		if constraint.maxcommonobject != -1 and constraint.maxcommonobject : errors.append(_('CONSTRAINT_CHECK_TOO_MANY_CHARACTERS'))
		if constraint.maxsameroom != -1 and constraint.maxsameroom : errors.append(_('CONSTRAINT_CHECK_TOO_MANY_CHARACTERS'))
		#extensions = models.ManyToManyField(DtExtension)
		'''
		return errors