
-- Parameters
insert into dt_parameters (id, name, `default`, configurable) values (1, 'current_turn', 0, 0);
insert into dt_parameters (id, name, `default`, configurable) values (2, 'phase', 0, 0); -- 1: Subscription to the challenge/tournament 2: Placement for challenge/tournament started, 3: Game in process for the challenge/Not used by tournament
insert into dt_parameters (id, name, `default`, configurable) values (201, 'all_round_same_time', 0, 1); -- 0: The round are run one after the other manually. 1: All challenges are created in the same time, players play when they want
insert into dt_parameters (id, name, `default`, configurable) values (202, 'repeat_characters', 0, 1); -- 0: Never / 1: Only alive / 2: Only alive or hurt / 3: Only out alive / 5: Only out alive or hurt / 6: All
insert into dt_parameters (id, name, `default`, configurable) values (203, 'repeat_objets', 0, 1); -- 0: Never / 1: Only alive / 3: Only out alive / 4: Only not out alive / 5: All
insert into dt_parameters (id, name, `default`, configurable) values (301, 'pv', 6, 3); -- 0: None, 1: Mine, 3: Both
insert into dt_parameters (id, name, `default`, configurable) values (302, 'players', 4, 3); -- 0: None, 1: Mine, 3: Both
insert into dt_parameters (id, name, `default`, configurable) values (303, 'show_placement_spawn', 2, 1); -- 0: None, 1: Mine, 3: Both
insert into dt_parameters (id, name, `default`, configurable) values (304, 'show_opponent_cards', 1, 1); -- 0: No, 1: Yes
insert into dt_parameters (id, name, `default`, configurable) values (305, 'random_rooms', 0, 1); -- 0: No, 1: Yes and hidden, 2: Yes and visible
insert into dt_parameters (id, name, `default`, configurable) values (306, 'clever_placement', 1, 1); -- 0: No, 1: Yes
insert into dt_parameters (id, name, `default`, configurable) values (307, 'taking_in_account_for_elo', 1, 1); -- 0: No, 1: Yes
insert into dt_parameters (id, name, `default`, configurable) values (308, 'max_cursed_object', -1, 1); -- -1: No limit, limit count otherwise
insert into dt_parameters (id, name, `default`, configurable) values (309, 'max_flying_characters', -1, 1); -- -1: No limit, limit count otherwise
insert into dt_parameters (id, name, `default`, configurable) values (310, 'max_dragons', -1, 1); -- -1: No limit, limit count otherwise
insert into dt_parameters (id, name, `default`, configurable) values (311, 'max_cycles', 6, 1); -- -1: No limit, limit count otherwise
insert into dt_parameters (id, name, `default`, configurable) values (312, 'time_per_turn', 180, 1); -- -1: No limit, limit count otherwise in second
insert into dt_parameters (id, name, `default`, configurable) values (400, 'player_num', -1, 1); -- -1: Player color
insert into dt_parameters (id, name, `default`, configurable) values (401, 'fight_0', -1, 1); -- -1: Player color
insert into dt_parameters (id, name, `default`, configurable) values (402, 'fight_1', 1, 1); -- -1: Player color
insert into dt_parameters (id, name, `default`, configurable) values (403, 'fight_2', 2, 1); -- -1: Player color
insert into dt_parameters (id, name, `default`, configurable) values (404, 'fight_3', 2, 1); -- -1: Player color
insert into dt_parameters (id, name, `default`, configurable) values (405, 'fight_4', 1, 1); -- -1: Player color
insert into dt_parameters (id, name, `default`, configurable) values (406, 'fight_5', 1, 1); -- -1: Player color
insert into dt_parameters (id, name, `default`, configurable) values (407, 'fight_6', 1, 1); -- -1: Player color
insert into dt_parameters (id, name, `default`, configurable) values (408, 'action_2', 1, 1); -- -1: Player color
insert into dt_parameters (id, name, `default`, configurable) values (409, 'action_3', 1, 1); -- -1: Player color
insert into dt_parameters (id, name, `default`, configurable) values (410, 'action_4', 1, 1); -- -1: Player color
insert into dt_parameters (id, name, `default`, configurable) values (411, 'action_5', 1, 1); -- -1: Player color
insert into dt_parameters (id, name, `default`, configurable) values (412, 'last_action_card', -1, 1); -- -1: Player color
insert into dt_parameters (id, name, `default`, configurable) values (413, 'last_combat_1', -1, 1); -- -1: Player color
insert into dt_parameters (id, name, `default`, configurable) values (414, 'last_combat_2', -1, 1); -- -1: Player color
insert into dt_parameters (id, name, `default`, configurable) values (415, 'score', 0, 1); -- -1: Player PV

