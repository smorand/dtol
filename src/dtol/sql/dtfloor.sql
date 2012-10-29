-- This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
-- Floors
-- walkable : -1 for not applicable, 0 for no, 1 for yes, 2 for yes with rope, 3 for yes special (water, bridge, tree, etc.)
-- ftype : -1 for not applicable, 0 for special, 1 for normal, 2 for obstacle, 3 for obstacle 3d, 4 notfranchable)
-- line of sight : 0 for no, 1 for yes, 2 for yes but stop, 3 for special
-- marqueur : a un marqueur associé
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (1, 'sol', 1, 1, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (2, 'twist', 1, 0, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (3, 'fosse', 2, 2, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (4, 'crevasse', 2, 2, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (5, 'eboulis', 0, 4, 0, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (6, 'chuttepierre', 1, 0, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (7, 'fontaine', 0, 3, 2, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (8, 'pentacle', 1, 0, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (9, 'eau', 3, 2, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (10, 'ponteau', 3, 2, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (11, 'lave', 3, 2, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (12, 'pontlave', 3, 2, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (13, 'escalier', 1, 0, 2, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (14, 'bibliotheque', 0, 3, 2, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (15, 'artefactantimagie', 0, 3, 2, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (16, 'tombeau', 0, 3, 2, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (17, 'sacre', -1, -1, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (18, 'tenebres', 3, 0, 3, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (19, 'tombe', 1, 3, 2, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (20, 'statue', 0, 3, 2, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (21, 'armurerie', 0, 3, 2, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (22, 'forge', 2, 2, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (23, 'piege_rouge', 3, 0, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (24, 'declencheur_rouge', 1, 0, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (25, 'piege_vert', 3, 0, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (26, 'declencheur_vert', 1, 0, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (27, 'piege_jaune', 3, 0, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (28, 'declencheur_jaune', 1, 0, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (29, 'piege_bleu', 3, 0, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (30, 'declencheur_bleu', 1, 0, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (31, 'trouultragravite', 2, 2, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (32, 'ultragravite', -1, -1, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (33, 'colonne', 0, 4, 0, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (34, 'cascade', 2, 2, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (35, 'pontbois', 1, 0, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (36, 'arbre', 1, 3, 2, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (37, 'arbrecoupe', 1, 0, 1, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (38, 'lianescorde', 1, 0, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (39, 'ponttroncarbre', 1, 0, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (40, 'canneaulave', 3, 2, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (41, 'tresor', 1, 0, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (42, 'canalisation', 3, 0, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (43, 'potionvitesse', 0, 3, 2, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (44, 'dolmen', 0, 3, 2, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (45, 'artefactdolmen', 0, 3, 2, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (46, 'pontcanneaulave', 3, 2, 2, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (47, 'pontglace', 1, 0, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (48, 'enneige', 1, 0, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (49, 'ice', 1, 0, 1, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (50, 'utilise', -1, -1, 1, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (51, 'pontbrise', 2, 2, 1, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (52, 'illusionfosse', 2, 2, 1, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (53, 'illusioneboulis', 0, 4, 3, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (54, 'arbrevivant', 1, 3, 2, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (55, 'liane', 1, 0, 1, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (56, 'ronces', 0, 4, 2, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (57, 'arbrecoupeneige', 1, 0, 1, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (58, 'pontglacefondu', 2, 2, 1, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (59, 'pontglacefondugele', 1, 0, 1, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (60, 't1_1', 1, 0, 1, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (61, 't1_2', 1, 0, 1, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (62, 't2_1', 1, 0, 1, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (63, 't2_2', 1, 0, 1, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (64, 't3_1', 1, 0, 1, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (65, 't3_2', 1, 0, 1, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (66, 'canalisationbrise', 2, 2, 1, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (67, 'trou', 2, 2, 1, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (68, 'dallerocher', 1, 0, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (69, 'orbe', 0, 3, 2, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (70, 'potionvie', 0, 3, 2, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (71, 'piege_violet', 3, 0, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (72, 'declencheur_violet', 1, 0, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (73, 'piege_vert2', 3, 0, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (74, 'declencheur_vert2', 1, 0, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (75, 'piege_orange', 3, 0, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (76, 'declencheur_orange', 1, 0, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (77, 'piege_bleu2', 3, 0, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (78, 'declencheur_bleu2', 1, 0, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (79, 'supertorche', 0, 3, 2, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (80, 'levierpontlevis', 1, 0, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (81, 'levierinverseur', 1, 0, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (82, 'coffre', 1, 3, 2, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (83, 'jarre', 1, -1, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (84, 'stalagtite', 1, 3, 2, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (85, 'rocher', 1, 3, 2, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (86, 'declencheur_orangeatre', 1, 0, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (87, 'trone', 0, 3, 2, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (88, 'eaupontlevis', 3, 0, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (89, 'pontlevis', 1, 0, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (90, 'filet', -1, 0, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (91, 'brume', -1, 0, 0, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (92, 'antimagie', -1, -1, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (93, 'mirroir_ne', -1, -1, 3, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (94, 'mirroir_se', -1, -1, 3, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (95, 'mirroir_so', -1, -1, 3, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (96, 'mirroir_no', -1, -1, 3, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (97, 'fletrissure', 0, -1, 3, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (98, 'tenebresmagiques', 3, 0, 3, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (99, 'verminophage', 3, 0, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (100, 'trouvermine', 1, 0, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (101, 'pentedouce_n', 3, 3, 3, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (102, 'pentedouce_e', 3, 3, 3, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (103, 'pentedouce_s', 3, 3, 3, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (104, 'pentedouce_o', 3, 3, 3, 0);
-- no vers se vide
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (105, 'triangle_1_v', -1, -1, 1, 0);
-- ne vers so vide
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (106, 'triangle_2_v', -1, -1, 1, 0);
-- no vers se bambou
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (107, 'triangle_1_b', -1, -1, 1, 0);
-- ne vers so bambou
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (108, 'triangle_2_b', -1, -1, 1, 0);
-- no vers se toit
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (109, 'triangle_1_t', -1, -1, 1, 0);
-- ne vers so toit
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (110, 'triangle_2_t', -1, -1, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (111, 'toit', -1, -1, -1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (112, 'tatami', 1, 1, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (113, 'broyeursol', 1, 1, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (114, 'broyeur', 0, 3, 2, 1);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (115, 'interrupteurbroyeur', 1, 0, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (116, 'rail', 1, 1, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (117, 'cellulemutant', 1, 0, 1, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (118, 'croixsainte', 0, 3, 2, 0);
insert into dt_floors (id, name, walkable, ftype, lineofsight, marker) values (119, 'piegeouvert', 0, 3, 2, 0);

