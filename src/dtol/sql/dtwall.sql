-- Walls
-- walkable : 0 for no, 1 for yes, 2 for special (portail)
-- lineofsight : 0 for no, 1 for yes, 2 for yes but only adjacent (meurtriere)
insert into dt_walls (id, name, walkable, lineofsight) values (1, 'vide', 1, 1);
insert into dt_walls (id, name, walkable, lineofsight) values (2, 'mur', 0, 0);
insert into dt_walls (id, name, walkable, lineofsight) values (3, 'murbrise', 1, 1);
insert into dt_walls (id, name, walkable, lineofsight) values (4, 'herse', 0, 0);
insert into dt_walls (id, name, walkable, lineofsight) values (5, 'hersebrisee', 1, 1);
insert into dt_walls (id, name, walkable, lineofsight) values (6, 'herseouverte', 1, 1);
insert into dt_walls (id, name, walkable, lineofsight) values (7, 'torche', 0, 0);
insert into dt_walls (id, name, walkable, lineofsight) values (8, 'torcheprise', 0, 0);
insert into dt_walls (id, name, walkable, lineofsight) values (9, 'meurtriere', 0, 2);
insert into dt_walls (id, name, walkable, lineofsight) values (10, 'passagesecret', 0, 0);
insert into dt_walls (id, name, walkable, lineofsight) values (11, 'toile', 0, 0);
insert into dt_walls (id, name, walkable, lineofsight) values (13, 'pentemontante', 0, 1);
insert into dt_walls (id, name, walkable, lineofsight) values (14, 'pentedescendante', 0, 1);
insert into dt_walls (id, name, walkable, lineofsight) values (15, 'cle', 0, 0);
insert into dt_walls (id, name, walkable, lineofsight) values (16, 'cleprise', 0, 0);
insert into dt_walls (id, name, walkable, lineofsight) values (17, 'portail', 2, 0);
insert into dt_walls (id, name, walkable, lineofsight) values (18, 'murportail', 0, 0);
