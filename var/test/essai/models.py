from django.db import models, transaction

'''
create table dt_games (id integer primary key auto_increment, name varchar(100), lasteventid integer);
create table dt_spawns (id integer primary key auto_increment, name varchar(100), game_id integer references game(id), lasteventid integer);
insert into dt_games values (1, 'game1', 8);
insert into dt_games values (2, 'game2', 10);
insert into dt_spawns values (1, 'spawn1', 1, 1);
insert into dt_spawns values (2, 'spawn2', 1, 1);
insert into dt_spawns values (3, 'spawn3', 1, 8);
insert into dt_spawns values (4, 'spawn1', 2, 1);
insert into dt_spawns values (8, 'spawn4', 2, 10);
'''

class DtGame(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	lasteventid = models.IntegerField()
	def spawns(self, lasteventidchoosen=None):
		if lasteventidchoosen is not None:
			return DtSpawn.objects.filter(game=self.id, lasteventid__gt=lasteventidchoosen).all()
		else:
			return DtSpawn.objects.filter(game=self.id).all()
	class Meta:
		db_table = u'dt_games'

class DtSpawn(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	game = models.ForeignKey(DtGame)
	lasteventid = models.IntegerField()
	class Meta:
		db_table = u'dt_spawns'
