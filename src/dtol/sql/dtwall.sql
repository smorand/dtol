-- This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
-- Walls
-- walkable : 0 for no, 1 for yes, 2 for special (portail)
-- line of sight : 0 for no, 1 for yes, 2 for yes but only adjacent (meurtriere), 3 for special (penteraide)
-- marqueur
insert into dt_walls (id, name, walkable, lineofsight, marker) values (1, 'vide', 1, 1, 0);
insert into dt_walls (id, name, walkable, lineofsight, marker) values (2, 'mur', 0, 0, 0);
insert into dt_walls (id, name, walkable, lineofsight, marker) values (3, 'murbrise', 1, 1, 1);
insert into dt_walls (id, name, walkable, lineofsight, marker) values (4, 'herse', 0, 0, 0);
insert into dt_walls (id, name, walkable, lineofsight, marker) values (5, 'hersebrisee', 1, 1, 1);
insert into dt_walls (id, name, walkable, lineofsight, marker) values (6, 'herseouverte', 1, 1, 1);
insert into dt_walls (id, name, walkable, lineofsight, marker) values (7, 'torche', 0, 0, 0);
insert into dt_walls (id, name, walkable, lineofsight, marker) values (8, 'torcheprise', 0, 0, 1);
insert into dt_walls (id, name, walkable, lineofsight, marker) values (9, 'meurtriere', 0, 2, 0);
insert into dt_walls (id, name, walkable, lineofsight, marker) values (10, 'passagesecret', 0, 0, 0);
insert into dt_walls (id, name, walkable, lineofsight, marker) values (11, 'toile', 0, 0, 1);
insert into dt_walls (id, name, walkable, lineofsight, marker) values (13, 'pentemontante', 0, 1, 0);
insert into dt_walls (id, name, walkable, lineofsight, marker) values (14, 'pentedescendante', 0, 1, 0);
insert into dt_walls (id, name, walkable, lineofsight, marker) values (15, 'cle', 0, 0, 0);
insert into dt_walls (id, name, walkable, lineofsight, marker) values (16, 'cleprise', 0, 0, 1);
insert into dt_walls (id, name, walkable, lineofsight, marker) values (17, 'portail', 2, 0, 1);
insert into dt_walls (id, name, walkable, lineofsight, marker) values (18, 'murportail', 0, 0, 1);
insert into dt_walls (id, name, walkable, lineofsight, marker) values (19, 'penteraidemontante', 0, 3, 0);
insert into dt_walls (id, name, walkable, lineofsight, marker) values (20, 'penteraidedescendante', 0, 3, 0);
insert into dt_walls (id, name, walkable, lineofsight, marker) values (21, 'bambou', 0, 0, 0);
