import os

from log import *
from player import *
from cards import *

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
		print "On the previous turn:" # fix to show all moves since player's last turn
		log.show(log.prev_lines)
		log.prev_lines = log.lines
		print "\n",
	
	raw_input("It's your turn now, %s! Hit ENTER to continue." % player.name)
	os.system('cls')

	if len(player.hand) == 0:
		deck.draw(player, 5)
		log.add("\nYou had an empty hand and drew 5 cards.", player)
	else:
		deck.draw(player, 2)
		log.add("\nYou drew 2 cards.", player)
	
	cards_played = 0

	while cards_played < 3:
		selection = hand_menu(player)

		if selection == 0:
			break
		
		log.add("\nYou played %s." % player.hand[selection - 1].name, player) # Refactor into card.play()
		card = player.hand.pop(selection - 1)
		
		if card.play(player):
			cards_played += 1
		else:
			print "\nYou can't play %s now!" % card.name
			player.hand.insert(selection - 1, card)

def hand_menu(player):
	player.show_hand()

	player.show_properties()

	print "What would you like to do, %s?" % player.name
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