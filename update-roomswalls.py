#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
#

import contextlib
import math
import sqlite3
import re

# config
INPUT_FILE = 'var/dtroomswalls.csv'
OUTPUT_FILE = 'src/dtol/sql/dtroomcase.sql'
DATABASE = 'src/resources/dtol.db'

# variables
rooms = dict()
tiles = dict()
floors = dict()
walls = dict()

# préchargement
con = sqlite3.connect(DATABASE)
cursor = con.cursor()
cursor.execute('select id, number, rotation from dt_rooms')
for row in cursor:
	rooms['%s-%d' % (row[1], row[2])] = row[0]
cursor.execute('select id, name from dt_tiles')
for row in cursor:
	tiles['%s' % (row[1])] = row[0]
cursor.execute('select id, name from dt_floors')
for row in cursor:
	floors['%s' % (row[1])] = row[0]
cursor.execute('select id, name from dt_walls')
for row in cursor:
	walls['%s' % (row[1])] = row[0]
con.close()

linecount = 0
with contextlib.nested(open(INPUT_FILE, 'r'), open(OUTPUT_FILE, 'w')) as (fin, fout):
	try:
		for line in fin:
			linecount += 1
			wallinfo = line.strip().split(';')
			floorinfo = wallinfo[3].split('-')
			if wallinfo[1][:5] != 'dalle':
				wall = {
					'id': int(wallinfo[0]),
					'room': rooms[wallinfo[1]],
					'x': (int(wallinfo[2])-1)%5,
					'y': math.floor((int(wallinfo[2])-1)/5),
					'floor': [ floors[m] for m in floorinfo ],
					'wall_nord': walls[wallinfo[4]],
					'wall_est': walls[wallinfo[5]],
					'wall_sud': walls[wallinfo[6]],
					'wall_ouest': walls[wallinfo[7]]
				}
				fout.write('insert into dt_rooms_cases (id, room_id, x, y, mur_nord_id, mur_est_id, mur_sud_id, mur_ouest_id) values (%d, %d, %d, %d, %d, %d, %d, %d);\n' % (wall['id'], wall['room'], wall['x'], wall['y'], wall['wall_nord'], wall['wall_est'], wall['wall_sud'], wall['wall_ouest']))
				for floor in wall['floor']:
					fout.write('insert into dt_rooms_cases_sol (dtroomcase_id, dtfloor_id) values (%d, %d);\n' % (wall['id'], floor))
			else:
				wall = {
					'id': int(wallinfo[0]),
					'room': tiles[re.sub(r'dalle.(.*)', 'dalle\\1', wallinfo[1])],
					'x': (int(wallinfo[2])-1)%5,
					'y': math.floor((int(wallinfo[2])-1)/5),
					'floor': [ floors[m] for m in floorinfo ],
					'wall_nord': walls[wallinfo[4]],
					'wall_est': walls[wallinfo[5]],
					'wall_sud': walls[wallinfo[6]],
					'wall_ouest': walls[wallinfo[7]]
				}
				fout.write('insert into dt_tiles_cases (id, tile_id, x, y, mur_nord_id, mur_est_id, mur_sud_id, mur_ouest_id) values (%d, %d, %d, %d, %d, %d, %d, %d);\n' % (wall['id'], wall['room'], wall['x'], wall['y'], wall['wall_nord'], wall['wall_est'], wall['wall_sud'], wall['wall_ouest']))
				for floor in wall['floor']:
					fout.write('insert into dt_tiles_cases_sol (dttilecase_id, dtfloor_id) values (%d, %d);\n' % (wall['id'], floor))
	except Exception as err:
		print linecount
		raise err
