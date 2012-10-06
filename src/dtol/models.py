# -*- coding: utf-8 -*-
#
# This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
#
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class DtExtension(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	class Meta:
		db_table = u'dt_extensions'

class DtParameter(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(unique=True, max_length=90)
	default = models.IntegerField()
	configurable = models.IntegerField()
	class Meta:
		db_table = u'dt_parameters'

class DtUser(models.Model):
	id = models.AutoField(primary_key=True)
	login = models.CharField(max_length=30, unique=True)
	password = models.CharField(max_length=100)
	email = models.CharField(max_length=100, unique=True)
	country = models.CharField(max_length=3)
	lang = models.CharField(max_length=6)
	zoom = models.IntegerField(default=10)
	elo = models.IntegerField(default=1500)
	creation = models.DateTimeField(auto_now_add=True)
	lastconnection = models.DateTimeField(auto_now=True, auto_now_add=True)
	connected = models.BooleanField(default=False)
	active = models.BooleanField(default=False)
	publicchallenge = models.BooleanField(default=True)
	publicprofile = models.BooleanField(default=True)
	packgraphique = models.CharField(max_length=255, default='')
	isadmin = models.BooleanField(default=False)
	primarycolor = models.CharField(max_length=20)
	secondarycolor = models.CharField(max_length=20)
	menujeu = models.IntegerField(default=0)
	extensions = models.ManyToManyField(DtExtension, through='DtUserExtension')
	class Meta:
		db_table = u'dt_users'

class DtUserExtension(models.Model):
	user = models.ForeignKey(DtUser)
	extension = models.ForeignKey(DtExtension)
	class Meta:
		db_table = u'dt_users_extensions'

class DtEmailChange(models.Model):
	id = models.AutoField(primary_key=True)
	key = models.CharField(max_length=50)
	email = models.CharField(max_length=100)
	user = models.ForeignKey(DtUser)
	date = models.DateTimeField(auto_now_add=True, db_index=True)
	class Meta:
		db_table = u'dt_email_changes'
		
class DtSponsored(models.Model):
	id = models.AutoField(primary_key=True)
	key = models.CharField(max_length=50)
	email = models.CharField(max_length=100)
	sponsor = models.ForeignKey(DtUser, related_name='sponsor')
	user = models.ForeignKey(DtUser, related_name='user', null=True)
	date = models.DateTimeField(auto_now_add=True, db_index=True)
	class Meta:
		db_table = u'dt_sponsored'

class DtLog(models.Model):
	id = models.AutoField(primary_key=True)
	date = models.DateTimeField(auto_now_add=True, db_index=True)
	user = models.ForeignKey(DtUser, null=True, db_index=True)
	factory = models.CharField(max_length=90, db_index=True)
	message = models.TextField(blank=True)
	class Meta:
		db_table = u'dt_log'

class DtChat(models.Model):
	id = models.AutoField(primary_key=True)
	date = models.DateTimeField(auto_now_add=True, db_index=True)
	user = models.ForeignKey(DtUser)
	message = models.TextField()
	class Meta:
		db_table = u'dt_chat'

class DtCharacter(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	deplacement = models.IntegerField()
	force = models.IntegerField()
	extensions = models.ManyToManyField(DtExtension, through='DtCharacterExtension')
	def capacities(self):
		return DtCharacterCapacity.objects.filter(id=self.id)
	class Meta:
		db_table = u'dt_characters'

class DtCharacterExtension(models.Model):
	dtcharacter = models.ForeignKey(DtCharacter)
	dtextension = models.ForeignKey(DtExtension)
	class Meta:
		db_table = u'dt_characters_extensions'

class DtCharacterCapacity(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	character = models.ForeignKey(DtCharacter, db_index=True)
	class Meta:
		db_table = u'dt_characters_capacities'
			
class DtObject(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	extensions = models.ManyToManyField(DtExtension, through='DtObjectExtension')
	def capacities(self):
		return DtObjectCapacity.objects.filter(id=self.id)
	class Meta:
		db_table = u'dt_objects'

class DtObjectExtension(models.Model):
	dtobject = models.ForeignKey(DtObject)
	dtextension = models.ForeignKey(DtExtension)
	class Meta:
		db_table = u'dt_objects_extensions'
	
class DtObjectCapacity(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	object = models.ForeignKey(DtObject, db_index=True)
	class Meta:
		db_table = u'dt_objects_capacities'

class DtFloor(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	walkable = models.IntegerField() # walkable : -1 for not applicable, 0 for no, 1 for yes, 2 for yes with rope, 3 for yes special (water, bridge, tree, etc.)
	ftype = models.IntegerField() # ftype : -1 for not applicable, 0 for special, 1 for normal, 2 for obstacle, 3 for obstacle 3d, 4 notfranchable)
	lineofsight = models.IntegerField() # line of sight : 0 for no, 1 for yes, 2 for yes but stop, 3 for special
	class Meta:
		db_table = u'dt_floors'

class DtWall(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	walkable = models.IntegerField() # walkable : 0 for no, 1 for yes, 2 for special (portail)
	lineofsight = models.IntegerField() # lineofsight : 0 for no, 1 for yes, 2 for yes but only adjacent (meurtriere)
	class Meta:
		db_table = u'dt_walls'

class DtRoomCategorie(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	class Meta:
		db_table = u'dt_room_categories'
		
class DtRoom(models.Model):
	id = models.AutoField(primary_key=True)
	number = models.CharField(max_length=4)
	rotation = models.IntegerField()
	categories = models.ManyToManyField(DtRoomCategorie, through='DtRoomCategorieRoom')
	extensions = models.ManyToManyField(DtExtension, through='DtRoomExtension')
	def cases(self):
		DtRoomCase.objects.filter(room=self.id)
	class Meta:
		db_table = u'dt_rooms'

class DtRoomCategorieRoom(models.Model):
	dtroom = models.ForeignKey(DtRoom)
	dtcategorie = models.ForeignKey(DtRoomCategorie)
	class Meta:
		db_table = u'dt_rooms_categories'

class DtRoomExtension(models.Model):
	dtroom = models.ForeignKey(DtRoom)
	dtextension = models.ForeignKey(DtExtension)
	class Meta:
		db_table = u'dt_rooms_extensions'

class DtTeam(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=150)
	user = models.ForeignKey(DtUser)
	modification = models.DateTimeField(auto_now=True, auto_now_add=True)
	characters = models.ManyToManyField(DtCharacter, through='DtTeamCharacter')
	objs = models.ManyToManyField(DtObject, through='DtTeamObject')
	rooms = models.ManyToManyField(DtRoom, through='DtTeamRoom')
	sack = models.ManyToManyField(DtObject, through='DtTeamObjectSack', related_name='sack')
	played = models.IntegerField(default=0)
	wins = models.IntegerField(default=0)
	lost = models.IntegerField(default=0)
	class Meta:
		db_table = u'dt_teams'

class DtTeamCharacter(models.Model):
	dtcharacter = models.ForeignKey(DtCharacter)
	dtteam = models.ForeignKey(DtTeam)
	class Meta:
		db_table = u'dt_teams_characters'

class DtTeamObject(models.Model):
	dtobject = models.ForeignKey(DtObject)
	dtteam = models.ForeignKey(DtTeam)
	class Meta:
		db_table = u'dt_teams_objects'

class DtTeamObjectSack(models.Model):
	sack = models.ForeignKey(DtObject)
	dtteam = models.ForeignKey(DtTeam)
	class Meta:
		db_table = u'dt_teams_objectssack'

class DtTeamRoom(models.Model):
	dtroom = models.ForeignKey(DtRoom)
	dtteam = models.ForeignKey(DtTeam)
	class Meta:
		db_table = u'dt_teams_rooms'


class DtRoomCase(models.Model):
	id = models.AutoField(primary_key=True)
	room = models.ForeignKey(DtRoom)
	x = models.IntegerField()
	y = models.IntegerField()
	sol = models.ManyToManyField(DtFloor, through='DtRoomCaseFloor')
	mur_nord = models.ForeignKey(DtWall, related_name='r_mur_nord')
	mur_est = models.ForeignKey(DtWall, related_name='r_mur_est')
	mur_sud = models.ForeignKey(DtWall, related_name='r_mur_sud')
	mur_ouest = models.ForeignKey(DtWall, related_name='r_mur_ouest')
	class Meta:
		db_table = u'dt_rooms_cases'

class DtRoomCaseFloor(models.Model):
	case = models.ForeignKey(DtRoomCase)
	floor = models.ForeignKey(DtFloor)
	class Meta:
		db_table = u'dt_roomcases_floors'

class DtTile(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=60)
	size = models.IntegerField()
	extensions = models.ManyToManyField(DtExtension, through='DtTileExtension')
	def cases(self):
		DtTileCase.objects.filter(tile=self.id)
	class Meta:
		db_table = u'dt_tiles'

class DtTileExtension(models.Model):
	dttile = models.ForeignKey(DtTile)
	dtextension = models.ForeignKey(DtExtension)
	class Meta:
		db_table = u'dt_tiles_extensions'

class DtTileCase(models.Model):
	id = models.AutoField(primary_key=True)
	tile = models.ForeignKey(DtTile)
	x = models.IntegerField()
	y = models.IntegerField()
	sol = models.ManyToManyField(DtFloor, through='DtTileCaseFloor')
	mur_nord = models.ForeignKey(DtWall, related_name='t_mur_nord')
	mur_est = models.ForeignKey(DtWall, related_name='t_mur_est')
	mur_sud = models.ForeignKey(DtWall, related_name='t_mur_sud')
	mur_ouest = models.ForeignKey(DtWall, related_name='t_mur_ouest')
	class Meta:
		db_table = u'dt_tiles_cases'

class DtTileCaseFloor(models.Model):
	case = models.ForeignKey(DtTileCase)
	floor = models.ForeignKey(DtFloor)
	class Meta:
		db_table = u'dt_tilecases_floors'

class DtSpawnState(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	class Meta:
		db_table = u'dt_spawns_states'

class DtGame(models.Model):
	id = models.AutoField(primary_key=True)
	parameters = models.ManyToManyField(DtParameter, through='DtGameParameter')
	def players(self):
		return DtPlayer.objects.filter(game=self.id)
	def characters(self, player=None):
		if player != None:
			return DtGameCharacter.objects.filter(game=self.id, player=player)
		else:
			return DtGameCharacter.objects.filter(game=self.id)
	def objects(self, player=None):
		if player != None:
			return DtGameObject.objects.filter(game=self.id, player=player)
		else:
			return DtGameObject.objects.filter(game=self.id)
	def rooms(self, player=None):
		return DtGameRoom.objects.filter(game=self.id)
	def tiles(self, player=None):
		return DtGameTile.objects.filter(game=self.id)
	def markers(self, player=None):
		return DtGameMarker.objects.filter(game=self.id)
	def messages(self, typ=None):
		if typ != None:
			return DtGameChat.objects.filter(game=self.id, type=typ)
		else:
			return DtGameChat.objects.filter(game=self.id)
	class Meta:
		db_table = u'dt_games'

class DtGameParameter(models.Model):
	game = models.ForeignKey(DtGame)
	parameter = models.ForeignKey(DtParameter)
	class Meta:
		db_table = u'dt_games_parameters'

class DtGameChat(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(DtUser)
	game = models.ForeignKey(DtGame)
	date = models.DateTimeField()
	message = models.TextField()
	type = models.IntegerField()
	class Meta:
		db_table = u'dt_game_chat'

class DtPlayer(models.Model):
	id = models.AutoField(primary_key=True)
	game = models.ForeignKey(DtGame)
	parameters = models.ManyToManyField(DtParameter, through='DtPlayerParameters')
	user = models.ForeignKey(DtUser)
	color = models.CharField(max_length=60)
	def characters(self):
		return DtGameCharacter.objects.filter(game=self.game, player=self.id)
	def objects(self):
		return DtGameObject.objects.filter(game=self.game, player=self.id)
	class Meta:
		db_table = u'dt_players'

class DtPlayerParameters(models.Model):
	player = models.ForeignKey(DtPlayer)
	parameter = models.ForeignKey(DtParameter)
	class Meta:
		db_table = u'dt_players_parameters'

class DtGameCharacter(models.Model):
	id = models.AutoField(primary_key=True)
	character = models.ForeignKey(DtCharacter)
	player = models.ForeignKey(DtPlayer)
	game = models.ForeignKey(DtGame)
	state = models.ForeignKey(DtSpawnState)
	x = models.IntegerField()
	y = models.IntegerField()
	class Meta:
		db_table = u'dt_games_characters'

class DtGameObject(models.Model):
	id = models.AutoField(primary_key=True)
	object = models.ForeignKey(DtObject)
	player = models.ForeignKey(DtPlayer)
	game = models.ForeignKey(DtGame)
	state = models.ForeignKey(DtSpawnState)
	x = models.IntegerField()
	y = models.IntegerField()
	class Meta:
		db_table = u'dt_game_objects'

class DtGameRoom(models.Model):
	id = models.AutoField(primary_key=True)
	game = models.ForeignKey(DtGame)
	room = models.ForeignKey(DtRoom)
	sens = models.IntegerField()
	rotation = models.IntegerField()
	x = models.IntegerField()
	y = models.IntegerField()
	class Meta:
		db_table = u'dt_game_rooms'

class DtGameTile(models.Model):
	id = models.AutoField(primary_key=True)
	game = models.ForeignKey(DtGame)
	tile = models.ForeignKey(DtTile)
	x = models.IntegerField()
	y = models.IntegerField()
	rotation = models.IntegerField()
	class Meta:
		db_table = u'dt_game_tiles'
	
class DtGameMarker(models.Model):
	id = models.AutoField(primary_key=True)
	game = models.ForeignKey(DtGame)
	marker = models.ForeignKey(DtFloor)
	x = models.IntegerField()
	y = models.IntegerField()
	class Meta:
		db_table = u'dt_game_markers'

class DtTeamConstraint(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=150)
	deleted = models.BooleanField(default=False)
	game = models.ForeignKey(DtGame, null=True, on_delete=models.CASCADE)
	protected = models.IntegerField(default=0)
	mincharacters = models.IntegerField(default=8)
	maxcharacters = models.IntegerField(default=8)
	minobjects = models.IntegerField(default=6)
	maxobjects = models.IntegerField(default=6)
	minrooms = models.IntegerField(default=2)
	maxrooms = models.IntegerField(default=2)
	mindeplacement = models.IntegerField(default=-1)
	maxdeplacement = models.IntegerField(default=-1)
	mintotaldeplacement = models.IntegerField(default=-1)
	maxtotaldeplacement = models.IntegerField(default=-1)
	minadvdeplacement = models.IntegerField(default=-1)
	maxadvdeplacement = models.IntegerField(default=-1)
	mintotaladvdeplacement = models.IntegerField(default=-1)
	maxtotaladvdeplacement = models.IntegerField(default=-1)
	minforce = models.IntegerField(default=-1)
	maxforce = models.IntegerField(default=-1)
	mintotalforce = models.IntegerField(default=-1)
	maxtotalforce = models.IntegerField(default=-1)
	minprestigious = models.IntegerField(default=-1)
	maxprestigious = models.IntegerField(default=-1)
	minspellcaster = models.IntegerField(default=-1)
	maxspellcaster = models.IntegerField(default=-1)
	minflying = models.IntegerField(default=-1)
	maxflying = models.IntegerField(default=-1)
	minintangible = models.IntegerField(default=-1)
	maxintangible = models.IntegerField(default=-1)
	mincursed = models.IntegerField(default=-1)
	maxcursed = models.IntegerField(default=-1)
	minshadowwalker = models.IntegerField(default=-1)
	maxshadowwalker = models.IntegerField(default=-1)
	minshadowroom = models.IntegerField(default=-1)
	maxshadowroom = models.IntegerField(default=-1)	
	minantimagicroom = models.IntegerField(default=-1)
	maxantimagicroom = models.IntegerField(default=-1)	
	minfountain = models.IntegerField(default=-1)
	maxfountain = models.IntegerField(default=-1)	
	mincounterfountain = models.IntegerField(default=-1)
	maxcounterfountain = models.IntegerField(default=-1)	
	minextensions = models.IntegerField(default=-1)
	maxextensions = models.IntegerField(default=-1)
	maxsamecharacter = models.IntegerField(default=-1)
	maxsameobject = models.IntegerField(default=-1)
	maxcommonobject = models.IntegerField(default=-1)
	maxsameroom = models.IntegerField(default=-1)
	extensions = models.ManyToManyField(DtExtension, through='DtTeamConstraintExtension')
	class Meta:
		db_table = u'dt_team_constraints'

class DtTeamConstraintExtension(models.Model):
	teamconstraint = models.ForeignKey(DtTeamConstraint)
	extension = models.ForeignKey(DtExtension)
	class Meta:
		db_table = u'dt_team_constraints_extensions'
