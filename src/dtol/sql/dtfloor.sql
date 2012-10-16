-- Floors
-- walkable : -1 for not applicable, 0 for no, 1 for yes, 2 for yes with rope, 3 for yes special (water, bridge, tree, etc.)
-- ftype : -1 for not applicable, 0 for special, 1 for normal, 2 for obstacle, 3 for obstacle 3d, 4 notfranchable)
-- line of sight : 0 for no, 1 for yes, 2 for yes but stop, 3 for special
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (1, 'sol', 1, 1, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (2, 'twist', 1, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (3, 'fosse', 2, 2, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (4, 'crevasse', 2, 2, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (5, 'eboulis', 0, 4, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (6, 'chuttepierre', 1, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (7, 'fontaine', 0, 3, 2);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (8, 'pentacle', 1, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (9, 'eau', 3, 2, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (10, 'ponteau', 3, 2, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (11, 'lave', 3, 2, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (12, 'pontlave', 3, 2, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (13, 'escalier', 1, 0, 2);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (14, 'bibliotheque', 0, 3, 2);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (15, 'artefactantimagie', 0, 3, 2);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (16, 'tombeau', 0, 3, 2);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (17, 'sacre', 1, 1, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (18, 'tenebres', 3, 0, 3);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (19, 'tombe', 1, 3, 2);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (20, 'statue', 0, 3, 2);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (21, 'armurerie', 0, 3, 2);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (22, 'forge', 2, 2, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (23, 'piege_rouge', 3, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (24, 'declencheur_rouge', 1, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (25, 'piege_vert', 3, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (26, 'declencheur_vert', 1, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (27, 'piege_jaune', 3, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (28, 'declencheur_jaune', 1, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (29, 'piege_bleu', 3, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (30, 'declencheur_bleu', 1, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (31, 'trouultragravite', 2, 2, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (32, 'ultragravite', -1, -1, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (33, 'colonne', 0, 4, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (34, 'cascade', 2, 2, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (35, 'pontbois', 1, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (36, 'arbre', 1, 3, 2);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (37, 'arbrecoupe', 1, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (38, 'lianescorde', 1, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (39, 'ponttroncarbre', 1, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (40, 'canneaulave', 3, 2, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (41, 'tresor', 1, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (42, 'canalisation', 3, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (43, 'potionvitesse', 0, 3, 2);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (44, 'dolmen', 0, 3, 2);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (45, 'artefactdolmen', 0, 3, 2);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (46, 'pontcaneaulave', 3, 2, 2);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (47, 'pontglace', 1, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (48, 'enneige', 1, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (49, 'ice', 1, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (50, 'utilise', -1, -1, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (51, 'pontbrise', 2, 2, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (52, 'illusionfosse', 2, 2, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (53, 'illusioneboulis', 0, 4, 3);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (54, 'arbrevivant', 1, 3, 2);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (55, 'liane', 1, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (56, 'ronces', 0, 4, 2);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (57, 'arbrecoupeneige', 1, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (58, 'pontglacefondu', 2, 2, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (59, 'pontglacefondugele', 1, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (60, 't1_1', 1, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (61, 't1_2', 1, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (62, 't2_1', 1, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (63, 't2_2', 1, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (64, 't3_1', 1, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (65, 't3_2', 1, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (66, 'canalisationbrise', 2, 2, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (67, 'trou', 2, 2, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (68, 'dallerocher', 1, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (69, 'orbe', 0, 3, 2);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (70, 'potionvie', 0, 3, 2);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (71, 'piege_violet', 3, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (72, 'declencheur_violet', 1, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (73, 'piege_orange', 3, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (74, 'declencheur_orange', 1, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (75, 'supertorche', 0, 3, 2);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (76, 'levierpontlevis', 1, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (77, 'levierinverseur', 1, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (78, 'coffre', 1, 3, 2);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (79, 'jarre', 1, -1, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (80, 'stalagtite', 1, 3, 2);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (81, 'rocher', 1, 3, 2);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (82, 'declencheur_orangeatre', 1, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (83, 'trone', 0, 3, 2);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (84, 'eaupontlevis', 3, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (85, 'pontlevis', 1, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (86, 'filet', -1, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (87, 'brume', -1, 0, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (88, 'antimagie', -1, -1, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (89, 'mirroir_ne', -1, -1, 3);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (90, 'mirroir_se', -1, -1, 3);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (91, 'mirroir_so', -1, -1, 3);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (92, 'mirroir_no', -1, -1, 3);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (93, 'fletrissure', 0, -1, 3);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (94, 'tenebresmagiques', 3, 0, 3);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (95, 'verminophage', 3, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (96, 'trouvermine', 1, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (97, 'pentedouce_n', 3, 3, 3);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (98, 'pentedouce_e', 3, 3, 3);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (99, 'pentedouce_s', 3, 3, 3);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (100, 'pentedouce_o', 3, 3, 3);
-- no vers se vide
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (101, 'triangle_1_v', -1, -1, 1);
-- ne vers so vide
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (102, 'triangle_2_v', -1, -1, 1);
-- no vers se bambou
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (103, 'triangle_1_b', -1, -1, 1);
-- ne vers so bambou
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (104, 'triangle_2_b', -1, -1, 1);
-- no vers se toit
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (105, 'triangle_1_t', -1, -1, 1);
-- ne vers so toit
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (106, 'triangle_2_t', -1, -1, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (107, 'toit', -1, -1, -1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (108, 'tatami', 1, 1, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (109, 'broyeursol', 1, 1, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (110, 'broyeur', 0, 3, 2);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (111, 'interrupteurbroyeur', 1, 0, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (112, 'rail', 1, 1, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight) values (113, 'cellulemutant', 1, 0, 1);

