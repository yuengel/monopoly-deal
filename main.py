from random import shuffle

from cards import *

class GameLog(object):

	def __init__(self):
		self.lines = 0
		self.history = []

	def add(self, player, string):
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

	def show_hand(self):
		num_card = 1
		for card in self.hand:
			print "%d: %s" % (num_card, card.name)
			num_card += 1


class Deck(object):

	def __init__(self, cards):
		self.cards = cards

	def deal(self, players, num):
		"""Deals num cards to each player given in the list players."""
		
		while num > 0:
			for player in players:
				player.hand.append(self.cards.pop())
			num -= 1

	## TODO: handle IndexError to deal with empty deck



def play_game():
	"""Main game loop."""
	
	game_won = False
	turns = 0
	
	deck.deal(players, 5)

	for player in players:
		print "\n%s:\n" % player.name
		player.show_hand()
	
	while not game_won:
		current_player = [players[turns % num_players]]
		turn(current_player)
		turns += 1
		
def turn(current_player):
	"""One turn. current_player should be a list with exactly one element."""

	player = current_player[0]
	cards_played = 0

	raw_input("\nOkay, it's %s's turn now! Hit ENTER." % player.name)

	if len(player.hand) == 0:
		deck.deal(current_player, 5)
		log.add(player, "You had an empty hand and drew 5 cards.")
	else:
		deck.deal(current_player, 2)
		log.add(player, "You drew 2 cards.")

	print "\n%s:\n" % player.name
	
	while cards_played < 3:
		player.show_hand()

		print "\nWhat would you like to do?"
		print "To play a card, select that card's number."
		print "Or to end your turn, select 0."
		selection = int(raw_input(": ")) # Catch ValueError

		if selection == 0:
			break

		while selection not in range(1, len(player.hand) + 1):
			selection = int(			 # Catch ValueError here too
				raw_input("That's not right. What would you like to do?\n: "))
		
		log.add(player, "You played %s." % player.hand[selection - 1].name) # Refactor into card.play()
		player.hand.pop(selection - 1).play()
		cards_played += 1



log = GameLog()
deck = Deck(assemble_deck())
players = []

shuffle(deck.cards)

num_players = int(raw_input("How many players (2-4)?\n: ")) # Factor out MAX_PLAYERS?
															# ValueError...					
while num_players not in range(2, 5):
	num_players = int(										# ValueError...
		raw_input("That's not right. How many players (2-4)?\n: "))

for num in range(num_players):
	player = Player(raw_input("Player %d's name: " % (num + 1)))
	players.append(player)

play_game()