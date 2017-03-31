import json
from random import shuffle

from log import *
from player import players

class Deck(object):

	def __init__(self):
		self.cards = self.assemble_deck()
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

	def assemble_deck(self):
		"""Returns a list of cards representing the whole game deck."""

		cards = []

		with open("cards.json") as f:
			raw_cards = json.load(f)

		for card in raw_cards:
			card_class = card.get("class")

			if card_class == "colored_property":
				new_card = ColoredProperty(
					card.get("name"), card.get("value"), card.get("kind"))
			elif card_class == "other_property":
				new_card = OtherProperty(
					card.get("name"), card.get("value"), card.get("kind"))
			elif card_class == "wild_property":
				new_card = WildProperty(
					card.get("name"), card.get("value"), card.get("kind"))
			elif card_class == "action":
				new_card = Action(
					card.get("name"), card.get("value"))
			elif card_class == "money":
				new_card = Money(
					card.get("name"), card.get("value"))

			cards.append(new_card)
		
		#  Prints list of cards for debugging
		#
		#  for card in cards:
		#  	   for attr in dir(card):
		#		   print "%s: %s" % (attr, getattr(card, attr))
		#	   print "\n",

		return cards


class Card(object):

	def __init__(self, name, value):
		self.name = name
		self.value = value

	def play(self, player):
		pass


class Property(Card):

	def __init__(self, name, value):
		super(Property, self).__init__(name, value)

	def play(self, player):
		for group in player.properties:
			try:
				has_matching = group[0].kind == self.kind and len(group) != group[0].full_size()
			except IndexError:
				print "Property.play() IndexError"
				continue

			if has_matching:
				print "\nDo you want to group %s with %s?" % (
					self.name, group[0].name)
				print "\t1. Yes"
				print "\t0. No"
				selection = raw_input(": ")

				while True:
					if selection == '1':
						group.append(self)
						return True
					elif selection == '0':
						break
					else:
						print "That's not right. Enter only 1 or 0."
						selection = raw_input(": ")

		new_group = []
		new_group.append(self)
		player.properties.append(new_group)
		return True

	def full_size(self):
		"""Returns the number of cards required to make a full set of this kind."""

		two = ['Brown', 'Dark Blue', 'Utility']
		three = ['Light Blue', 'Pink', 'Orange', 'Red', 'Yellow', 'Green']
		four = ['Railroad']

		if self.kind in two:
			return 2
		if self.kind in three:
			return 3
		if self.kind in four:
			return 4


class ColoredProperty(Property):

	def __init__(self, name, value, kind):
		super(ColoredProperty, self).__init__(name, value)
		self.kind = kind

	def __dir__(self):
		return ['name', 'value', 'kind']


class OtherProperty(Property):

	def __init__(self, name, value, kind):
		super(OtherProperty, self).__init__(name, value)
		self.kind = kind

	def __dir__(self):
		return ['name', 'value', 'kind']


class WildProperty(Property):

	def __init__(self, name, value, kinds):
		super(WildProperty, self).__init__(name, value)
		self.kinds = kinds
		self.kind = self.kinds[0]

	def __dir__(self):
		return ['name', 'value', 'kinds']

	def play(self, player):
		print "\nWhich kind do you want to play %s as?" % self.name

		num_kinds = 1
		for kind in self.kinds:
			print "\t%d: %s" % (num_kinds, kind)
			num_kinds += 1

		selection = None
		while True:
			try:
				selection = int(raw_input(": "))
				if selection in range(1, num_kinds):
					break
			except ValueError:
				pass
			
			print "Try again, it looks like you mistyped."

		self.kind = self.kinds[selection - 1]
		return Property.play(self, player)


class Action(Card):

	def __init__(self, name, value):
		super(Action, self).__init__(name, value)
		self.kind = self.name

	def __dir__(self):
		return ['name', 'value']


	def play(self, player):
		print "\nDo you want to bank this %s for $%dM?" % (self.name, self.value)
		print "\t1. Yes"
		print "\t0. No"
		selection = raw_input(": ")

		while True:
			if selection == '1':
				player.bank.append(self)
				player.bank_value += self.value
				break
			elif selection == '0':
				break
			else:
				print "That's not right. Enter only 1 or 0."
				selection = raw_input(": ")

		if self.name == "Deal Breaker":
			if self.deal_breaker(player):
				log.add("You played %s." % self.name, player)
				discards.append(self)
				return True
			else:
				return False
		elif self.name == "Forced Deal":
			return self.forced_deal(player)
		elif self.name == "Sly Deal":
			return self.sly_deal(player)
		elif self.name == "Just Say No":
			return self.just_say_no(player)
		elif self.name == "Debt Collector":
			return self.debt_collector(player)
		elif self.name == "It's My Birthday":
			log.add("You played %s." % self.name, player)
			if self.its_my_birthday(player):
				discards.append(self)
				return True
			else:
				return False # Remove logs referring to the play?
		elif self.name == "Double the Rent":
			return self.double_the_rent(player)
		elif self.name == "House":
			return self.house(player)
		elif self.name == "Hotel":
			return self.hotel(player)
		elif self.name == "Pass GO":
			if self.pass_go(player):
				log.add("You played %s and drew 2 cards." % self.name, player)
				discards.append(self)
				return True
			else:
				return False

	def deal_breaker(self, player):
		
		all_full_sets = []
		owner_of = {}
		num_set = 0

		# Assemble list of valid sets to choose from
		for other in players:
			if other is not player:
				full_sets = other.get_full_sets()
				
				for x in range(0, len(full_sets)):
					num_set += 1
					owner_of[num_set] = other

				all_full_sets.extend(full_sets)

		if len(all_full_sets) == 0:
			print "\nYou can't play %s now!" % self.name
			return False

		num_set = 0
		for full_set in all_full_sets:
			num_set += 1
			print "\n\t%d:" % num_set,
			for card in full_set:
				print "%s  " % card.name,

		print "\n\nWhich set would you like to steal?"
		print "\t0. Cancel."

		selection = None
		while True:
			try:
				selection = int(raw_input(": "))
				if selection in range(0, num_set + 1):
					break
			except ValueError:
				pass

			print "Try again, it looks like you mistyped."

		if selection == 0:
			return False

		set_paid = owner_of[selection].pay_full_set(all_full_sets[selection - 1])
		player.properties.append(set_paid)
		return True

	def forced_deal(self, player):
		return True

	def sly_deal(self, player):
		return True

	def just_say_no(self, player):
		return True

	def debt_collector(self, player):
		return True

	def its_my_birthday(self, player):
		cards_paid = []
		lines_back = 1

		for other in players:
			if other is not player and other.has_assets():
				log.prompt(other, log.lines - lines_back)
				new_cards = other.pay(2, player)
				for card in new_cards:
					log.add("%s paid %s." % (other.name, card.name), other)
					lines_back += 1
				cards_paid.extend(new_cards)

		if len(cards_paid) == 0:
			print "\nYou can't play %s now!" % card.name
			return False

		log.prompt(player, log.lines - lines_back)
		player.receive(cards_paid)
		return True

	def double_the_rent(self, player):
		return True

	def house(self, player):
		return True

	def hotel(self, player):
		return True

	def pass_go(self, player):
		deck.draw(player, 2)
		return True


class Money(Card):

	def __init__(self, name, value):
		super(Money, self).__init__(name, value)

	def __dir__(self):
		return ['name', 'value']

	def play(self, player):
		player.bank.append(self)
		player.bank_value += self.value
		log.add("You banked %s." % self.name, player)
		return True


deck = Deck()
discards = []