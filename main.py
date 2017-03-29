from random import shuffle

from cards import *

class Player(object):

	def __init__(self, name):
		self.name = name
		self.hand = []


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
		for card in player.hand:
			print card.name
	
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
	else:
		deck.deal(current_player, 2)

	print "\n%s:\n" % player.name
	
	while cards_played < 3:
		num_card = 1
		for card in player.hand:
			print "%d: %s" % (num_card, card.name)
			num_card += 1

		print "\nWhat would you like to do?"
		print "To play a card, select that card's number."
		selection = int(raw_input(": ")) # Catch ValueError

		while selection not in range(1, num_card):
			selection = int(			 # Catch ValueError here too
				raw_input("That's not right. What would you like to do?\n: "))
		
		print "You chose to play card %d." % selection
		player.hand.pop(selection - 1).play()
		cards_played += 1
		print cards_played



deck = Deck(assemble_deck())
shuffle(deck.cards)

players = []
num_players = int(raw_input("How many players (2-4)?\n: ")) # Factor out MAX_PLAYERS?

while num_players not in range(2, 5):
	num_players = int(
		raw_input("That's not right. How many players (2-4)?\n: "))

for num in range(num_players):
	player = Player(raw_input("Player %d's name: " % (num + 1)))
	players.append(player)

play_game()