# -*- coding: utf-8 -*-
#
# This file is covered by the GNU Public Licence v3 licence. See http://www.gnu.org/licenses/gpl.txt
#

import commons
import random
random.seed()

class Tournament(object):
	'''
	Manage a tournament
	'''

	def __init__(self, players):
		self._players = players
		if len(players)%2 == 1: # Add a fictive player if odd number of player
			self._players.append(None)
		
	def calculateGames(self, mixPlayer=True, mixRounds=True, mixGameInRound=True, mixPlayerInGame=True):
		'''
		This method returns the list of game for the list of players chosen
		The return is :
		[ [ (Player1, Player2), (Player3, Player3), ... ], [ ... ] ]
		This is a list of round, every round is composed of games, a game is composed of 2 players
		@param mixPlayer: If true the players will be randomly permuted to calculate the games 
		@param mixRounds: If true when all the rounds have been calculated, the order of rounds is randomly permuted
		@param mixGameInRound: If true, when a round is over, the game are randomly permuted
		@param mixPlayerInGame: If true the first player of every game is randomly chosen
		@return: The list of rounds with permutation asked
		'''
		# Step one : prepare variable and create permutation of rounds and player
		numberOfPlayers = len(self._players)
		permutationPlayer = [ i for i in range (numberOfPlayers) ]
		# Step 2; Create all combinaison of games
		games = [ (i, j) for i in range(numberOfPlayers) for j in range(i+1, numberOfPlayers) ]
		playedGames = [] # Games already played
		playedToday= [] # Player having make a game in the current round
		rounds = [ [] for i in range(numberOfPlayers-1) ] # Rounds
		r = 0 # Current rounds
		m = 0
		# While all the game are not in a round, we add game in the round. A game can be added in the round only if it's not already played
		# and if the player have not participate in the round
		# If we cannot complete the round, we go back and remove the last inserted game to add the next one in the lists
		while len(playedGames) != len(games):
			if games[m][0] not in playedToday and games[m][1] not in playedToday and m not in playedGames:
				# Permutate player in the game if asked
				g = (self._players[permutationPlayer[games[m][0]]], self._players[permutationPlayer[games[m][1]]])
				if mixPlayerInGame and random.randint(0, 1) == 0: g = (self._players[permutationPlayer[games[m][1]]], self._players[permutationPlayer[games[m][0]]])
				rounds[r].append(g)
				playedGames.append(m)
				playedToday.append(games[m][0])
				playedToday.append(games[m][1])
			m += 1
			if len(rounds[r]) == numberOfPlayers/2:
				# Round is completed, prepare the next one
				r += 1
				m = 0
				playedToday = []
			elif m == len(games):
				# We can't complete the round because no game not played can be played (all players are already playing).
				# So we remove the last choosen game to try new combinaison of game
				rounds[r].pop()
				m = playedGames.pop()+1
				playedToday.pop()
				playedToday.pop()
		# Permutation of rounds in the list or game in the round if asked
		if mixRounds: commons.permutateonplace(rounds)
		if mixGameInRound:
			for r in rounds: commons.permutateonplace(r)
		return rounds
				
		
