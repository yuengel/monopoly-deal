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
	
	player.cards_played = 0
	turn_menu(player)
	player.prev_move = log.lines

def turn_menu(player):
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
		hand_menu(player)
		if player.cards_played == 3:
			return
	elif selection == 2:
		board_menu()
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

	turn_menu(player)

def hand_menu(player):
	
	os.system('cls')

	while player.cards_played < 3:	
		num_card = 0
		print "\n",
		for card in player.hand:
			num_card += 1

			if isinstance(card, Money):
				print "\t%d: %s" % (num_card, card.name)
			elif isinstance(card, Rent):
				print "\t%d: %s: %s - $%dM" % (num_card, card.name, card.kind, card.value)
			elif isinstance(card, Action) or isinstance(card, WildProperty):
				print "\t%d: %s - $%dM" % (num_card, card.name, card.value)
			else: # is non-Wild Property
				print "\t%d: %s: %s - $%dM" % (num_card, card.name, card.kind, card.value)
			
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
			return

		card = player.hand.pop(selection - 1)
			
		if card.play(player):
			player.cards_played += 1
		else:
			player.hand.insert(selection - 1, card)

	os.system('cls')

def board_menu():
	os.system('cls')

	for one_player in players:
		print "%s's properties:" % one_player.name
		for group in one_player.properties:
			for card in group:
				print "\t%s (%s) - $%dM" % (card.name, card.kind, card.value)
			print "\n",

		print "%s's bank:" % one_player.name
		for bill in one_player.bank:
			if "$" not in bill.name:
				print "\t%s ($%dM)" % (bill.name, bill.value)
			else:
				print "\t%s" % bill.name
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