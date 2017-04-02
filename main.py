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
	
	if player.prev_move != 0:
		log.prompt(player, player.prev_move, "Since your previous turn:")
	else:
		log.prompt(player)

	if len(player.hand) == 0:
		deck.draw(player, 5)
		log.add("You had an empty hand and drew 5 cards.", player)
	else:
		deck.draw(player, 2)
		log.add("You drew 2 cards.", player)
	
	cards_played = 0
	turn_menu(player, cards_played)
	player.prev_move = log.lines

def turn_menu(player, cards_played):
	print "\nWhat would you like to do, %s?" % player.name
	print "\t1. Play a card from your hand."
	print "\t2. View the game board."
	print "\t3. Move a card you've played."
	print "\t4. View the discard pile."
	print "\t5. View the game log."
	print "\t0. End your turn."

	selection = None
	while True:
		try:
			selection = int(raw_input(": "))
			if selection in range(0, 6):
				break
		except ValueError:
			pass
			
		print "Try again, it looks like you mistyped."

	if selection == 1:
		cards_played = hand_menu(player, cards_played)
		if cards_played == 3:
			return
	elif selection == 2:
		board_menu(player)
	elif selection == 3:
		player.reorganize()
	elif selection == 4:
		os.system('cls')
		for card in discards:
			print card.name
	elif selection == 5:
		os.system('cls')
		log.show()
	elif selection == 0:
		return

	turn_menu(player, cards_played)

def hand_menu(player, cards_played):
	
	os.system('cls')

	while cards_played < 3:	
		player.show_hand()
		print "\t0: Go back."
		print "\nWhich card would you like to play, %s?" % player.name

		selection = None
		while True:
			try:
				selection = int(raw_input(": "))
				if selection in range(0, len(player.hand) + 1):
					break
			except ValueError:
				pass
				
			print "Try again, it looks like you mistyped."

		if selection == 0:
			os.system('cls')
			return cards_played

		card = player.hand.pop(selection - 1)
			
		if card.play(player):
			cards_played += 1
		else:
			player.hand.insert(selection - 1, card)

	os.system('cls')
	return cards_played

def board_menu(player):
	os.system('cls')

	for one_player in players:
		print "\n%s's properties:" % one_player.name
		one_player.show_properties()
		print "%s's bank:" % one_player.name
		for bill in one_player.bank:
			print "\t%s" % bill.name,
		print "\n",

	raw_input("\n: ")
	return


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
	# TODO: Strip whitespace from player name input
	player = Player(raw_input("Player %d's name: " % (num + 1)))
	
	for one_player in players:
		while player.name == one_player.name:
			print "Try again, two players can't have the same name."
			player = Player(raw_input(": "))

	players.append(player)

play_game()