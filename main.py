import os
from random import shuffle

from cards import *

class GameLog(object):

	def __init__(self):
		self.prev_lines = 0
		self.lines = 0
		self.history = []

	def add(self, string, player):
		print string
		string = string.replace("You", player.name)
		self.history.append(string)
		self.lines += 1
		
	def show(self, start=0):
		for line in range(start, self.lines):
			print line, self.history[line]


class Player(object):

	def __init__(self, name):
		self.name = name
		self.hand = []
		self.properties = []
		self.bank = []
		self.bank_value = 0

	def show_hand(self):
		num_card = 1
		print "\n",
		for card in self.hand:
			print "%d: %s" % (num_card, card.name)
			num_card += 1


class Deck(object):

	def __init__(self, cards):
		self.cards = cards
		shuffle(self.cards)

	def deal(self, players, num):
		"""Deals num cards to each player given in the list players."""
		
		while num > 0:
			for player in players:
				self.draw(player, 1)
			num -= 1

	def draw(self, player, num):
		"""Deals num cards to player (given as Player object). """
		
		while num > 0:

			if len(self.cards) == 0:
				self.cards = discards
				discards = []
				shuffle(self.cards)

			player.hand.append(self.cards.pop())
			num -= 1



def play_game():
	"""Main game loop."""
	
	game_won = False
	turns = 0
	
	deck.deal(players, 5)
	
	while not game_won:
		player = players[turns % num_players]
		turn(player)
		turns += 1
		
def turn(player):
	os.system('cls')
	
	if log.lines != 0:
		print "On the previous turn:"
		log.show(log.prev_lines)
		log.prev_lines = log.lines
	
	raw_input("It's your turn now, %s! Hit ENTER to continue." % player.name)
	os.system('cls')

	if len(player.hand) == 0:
		deck.draw(player, 5)
		log.add("You had an empty hand and drew 5 cards.", player)
	else:
		deck.draw(player, 2)
		log.add("You drew 2 cards.", player)
	
	cards_played = 0

	while cards_played < 3:
		selection = hand_menu(player)

		if selection == 0:
			break
		
		log.add("You played %s." % player.hand[selection - 1].name, player) # Refactor into card.play()
		card = player.hand.pop(selection - 1)
		
		if card.play(player):
			cards_played += 1
		else:
			print "You can't play %s now!" % card.name
			player.hand.insert(selection - 1, card)

def hand_menu(player):
	player.show_hand()

	for group in player.properties:
		for card in group:
			print card.name,
		print "\n"

	print "\nWhat would you like to do, %s?" % player.name
	print "To play a card, select that card's number."
	print "Or to end your turn, select 0."

	selection = None
	while True:
		try:
			selection = int(raw_input(": "))
			if selection in range(0, len(player.hand) + 1):
				break
		except ValueError:
			pass
			
		print "Try again, it looks like you mistyped."

	return selection



log = GameLog()
players = []
deck = Deck(assemble_deck())
discards = []

print "How many players? (2-4)" # Factor out max_players?

num_players = None
while True:
	try:
		num_players = int(raw_input(": "))
		if num_players in range(2, 5):
			break
	except ValueError:
		pass
			
	print "Try again, it looks like you mistyped."

for num in range(num_players):
	player = Player(raw_input("Player %d's name: " % (num + 1)))
	players.append(player)

play_game()