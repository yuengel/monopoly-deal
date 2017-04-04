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
			elif card_class == "rent":
				new_card = Rent(
					card.get("name"), card.get("value"), card.get("kind"))
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
			full_with_buildings = group[0].full_size()
			if self.name == "House":
				full_with_buildings += 1
			if self.name == "Hotel":
				full_with_buildings += 2

			try:
				has_matching = group[0].kind == self.kind and len(group) < full_with_buildings
			except IndexError:
				print "Property.play() IndexError"
				continue

			if has_matching:
				if self.name == "House" or self.name == "Hotel":
					if len(group) == full_with_buildings - 1:
						group.append(self)
						log.add("You played %s in a group with %s." 
							% (self.name, group[0].name), player)
						return True
					else:
						break

				print "\nDo you want to group %s with %s?" % (
					self.name, group[0].name)
				print "\t1. Yes"
				print "\t0. No"
				selection = raw_input(": ")

				while True:
					if selection == '1':
						group.append(self)
						log.add("You played %s\nin a group with %s (%s)." 
							% (self.name,  group[0].name, self.kind), player)
						return True
					elif selection == '0':
						break
					else:
						print "Try again, it looks like you mistyped."
						selection = raw_input(": ")

		if self.name == "House" or self.name == "Hotel":
			self = Money(self.name, self.value)
			self.play(player)
			return True

		if hasattr(self, 'kinds') and len(self.kinds) == 10: # indicating Wild: Any card
			print "\nYou can't play %s by itself!" % self.name
			return False
		
		new_group = []
		new_group.append(self)
		player.properties.append(new_group)
		log.add("You played %s (%s)." % (self.name, self.kind), player)
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

	def rents_for(self, num_properties):
		"""Returns the rate a given property set rents for, given
		how many properties are in the set (not including buildings).
		"""

		rent_dict = {
		"Brown": [1, 2],
		"Light Blue": [1, 2, 3],
		"Pink": [1, 2, 4],
		"Orange": [1, 3, 5],
		"Red": [2, 3, 6],
		"Yellow": [2, 4, 6],
		"Green": [2, 4, 7],
		"Dark Blue": [3, 8],
		"Railroad": [1, 2, 3, 4],
		"Utility": [1, 2]}
		
		return rent_dict[self.kind][num_properties]


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

	def __dir__(self):
		return ['name', 'value']


	def play(self, player):
		print "\nDo you want to bank this %s for $%dM?" % (self.name, self.value)
		print "\t1. Yes"
		print "\t0. No"
		selection = raw_input(": ")

		while True:
			if selection == '1':
				self = Money(self.name, self.value)
				self.play(player)
				return True
			elif selection == '0':
				break
			else:
				print "That's not right. Enter only 1 or 0."
				selection = raw_input(": ")

		if self.name == "Deal Breaker":
			return self.deal_breaker(player)

		elif self.name == "Forced Deal":
			return self.forced_deal(player)
			
		elif self.name == "Sly Deal":
			return self.sly_deal(player)

		elif self.name == "Just Say No":
			print "\nYou can't play %s now!" % self.name
			return False

		elif self.name == "Debt Collector":
			return self.debt_collector(player)

		elif self.name == "It's My Birthday":
			return self.its_my_birthday(player)

		elif self.name == "Double the Rent":
			print "\nYou can't play %s now!" % self.name
			return False

		elif self.name == "House":
			return self.house(player)

		elif self.name == "Hotel":
			return self.hotel(player)

		elif self.name == "Pass GO":
			return self.pass_go(player)

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
			print "\n\t%d: %s's %s set:" % (
				num_set, owner_of[num_set].name, full_set[0].kind)
			for card in full_set:
				print "\t%s" % card.name

		print "\n\t0. Cancel."
		print "\n\nWhich set would you like to steal?"

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

		log.add("You played %s." % self.name, player)
		log.prompt(owner_of[selection], log.lines - 1)

		if owner_of[selection].just_say_no(player):
			log.add("You played Just Say No, blocking %s's %s."
				% (player.name, self.name), other)
			log.prompt(player, log.lines - 1)
		else:
			log.prompt(player, log.lines)
			owner_of[selection].properties.remove(all_full_sets[selection - 1])
			player.receive(all_full_sets[selection - 1])
		
		discards.append(self)
		return True

	def forced_deal(self, player):
		for other in players:
			no_sets = other.filter_properties('no_full_sets')
			other_properties_list = other.get_properties(no_sets)

			if other is not player and other_properties_list:
				print "\nTrade properties with %s?" % other.name
				print "\t1. Yes."
				print "\t0. No."
				selection = raw_input(": ")

				while True:
					if selection == '1':
						num_properties = 0
						for card in other_properties_list:
							num_properties += 1
							print "\t%d: %s" % (num_properties, card.name)

						print "\t0. Cancel."
						print "\nWhich property would you like to take?"

						selection = None
						while True:
							try:
								selection = int(raw_input(": "))
								print selection
								if selection in range(0, len(other_properties_list) + 1):
									break
							except ValueError:
								pass

							print "Try again, it looks like you mistyped."

						if selection == 0:
							return False

						no_buildings = player.filter_properties('no_buildings')
						player_properties_list = player.get_properties(no_buildings)
						
						num_properties = 0
						for card in player_properties_list:
							num_properties += 1
							print "\t%d: %s (%s) - $%dM" % (
								num_properties, card.name, card.kind, card.value)

						print "\t0. Cancel."
						print "\nWhich property would you like to give in exchange?"

						selection_two = None
						while True:
							try:
								selection_two = int(raw_input(": "))
								if selection_two in range(0, num_properties + 1):
									break
							except ValueError:
								pass

							print "Try again, it looks like you mistyped."

						if selection_two == 0:
							return False
						
						log.add("You played %s." % self.name, player)
						log.prompt(other, log.lines - 1)
						
						if other.just_say_no(player, other_properties_list[selection - 1].name):
							log.add("You played Just Say No, blocking %s's %s."
								% (player.name, self.name), other)
							log.prompt(player, log.lines - 1)
						else:
							own_new_card = other.pay_one(
								no_sets.get(selection - 1))
							other_new_card = player.pay_one(
								no_buildings.get(selection_two - 1))
							log.add("You gave up %s (%s)." % (
								own_new_card.name, own_new_card.kind), other)
							other.receive([other_new_card])
							log.prompt(player, log.lines - 2)
							log.add("You gave up %s (%s)." % (
								other_new_card.name, other_new_card.kind), player)
							player.receive([own_new_card])

						discards.append(self)
						return True
					elif selection == '0':
						break
					else:
						print "Try again, it looks like you mistyped."
						selection = raw_input(": ")
		
		print "\nYou can't play %s now!" % self.name
		return False

	def sly_deal(self, player):
		for other in players:
			no_sets = other.filter_properties('no_full_sets')
			properties_list = other.get_properties(no_sets)

			if other is not player and properties_list:
				print "\nSteal a property from %s?" % other.name
				print "\t1. Yes."
				print "\t0. No."
				selection = raw_input(": ")

				while True:
					if selection == '1':
						num_properties = 0
						for card in properties_list:
							num_properties += 1
							print "\t%d: %s (%s) - $%dM" % (
								num_properties, card.name, card.kind, card.value)

						print "\t0. Cancel."
						print "\nWhich property would you like to take?"

						selection = None
						while True:
							try:
								selection = int(raw_input(": "))
								print selection
								if selection in range(0, len(properties_list) + 1):
									break
							except ValueError:
								pass

							print "Try again, it looks like you mistyped."

						if selection == 0:
							return False

						log.add("You played %s." % self.name, player)
						log.prompt(other, log.lines - 1)
						
						if other.just_say_no(player, properties_list[selection - 1].name):
							log.add("You played Just Say No, blocking %s's %s."
								% (player.name, self.name), other)
							log.prompt(player, log.lines - 1)
						else:
							new_card = other.pay_one(
								no_sets.get(selection - 1))
							log.add("You gave up %s (%s)." % (
								new_card.name, new_card.kind), other)
							log.prompt(player, log.lines - 1)
							player.receive([new_card])
						
						discards.append(self)
						return True
					elif selection == '0':
						break
					else:
						print "Try again, it looks like you mistyped."
						selection = raw_input(": ")

		print "\nYou can't play %s now!" % self.name
		return False

	def just_say_no(self, player, target):
		player.hand.remove(self)
		discards.append(self)

		log.prompt(target, log.lines - 1)
		return not target.just_say_no(player)

	def debt_collector(self, player):
		cards_paid = []
		lines_back = 1

		for other in players:
			if other is not player and other.has_assets():
				print "\nCollect from %s?" % other.name
				print "\t1. Yes."
				print "\t0. No."
				selection = raw_input(": ")
			
				while True:
					if selection == '1':
						log.add("You played %s." % self.name, player)
						log.prompt(other, log.lines - lines_back)

						if other.just_say_no(player, "$5M"):
							log.add("You played Just Say No, blocking %s's %s." % (
								player.name, self.name), other)
							lines_back += 1
						else:
							cards_paid = other.pay(5, player)
							for card in cards_paid:
								log.add("You paid %s." % card.name, other)
								lines_back += 1

						log.prompt(player, log.lines - lines_back + 1)
						player.receive(cards_paid)
						discards.append(self)
						return True
					elif selection == '0':
						break
					else:
						print "Try again, it looks like you mistyped."
						selection = raw_input(": ")

		print "\nYou can't play %s now!" % self.name
		return False

	def its_my_birthday(self, player):
		cards_paid = []
		lines_back = 1

		log.add("You played %s." % self.name, player)

		for other in players:
			if other is not player and other.has_assets():
				log.prompt(other, log.lines - lines_back)
				if other.just_say_no(player, "$2M"):
					log.add("You played Just Say No, blocking %s's %s." % (
						player.name, self.name), other)
					lines_back += 1
				else:
					new_cards = other.pay(2, player)
					for card in new_cards:
						log.add("%s paid %s." % (other.name, card.name), other)
						lines_back += 1

					cards_paid.extend(new_cards)

		if not cards_paid:
			log.remove()
			print "\nYou can't play %s now!" % self.name
			return False

		log.prompt(player, log.lines - lines_back + 1)
		player.receive(cards_paid)
		discards.append(self)
		return True

	def double_the_rent(self, player):
		player.hand.remove(self)
		discards.append(self)
		return True

	def house(self, player):
		full_sets = player.get_full_sets()
		to_remove = []
		for a_set in full_sets:
			for card in a_set:

				if card.name == "House":
					to_remove.append(a_set)
					break

			if not isinstance(a_set[0], (ColoredProperty, WildProperty)):
				to_remove.append(a_set)

		full_sets = [a_set for a_set in full_sets if a_set not in to_remove]		
		if not full_sets:
			print "\nYou can't play %s now!" % self.name
			return False

		num_sets = 0
		for a_set in full_sets:
			num_sets += 1
			print "\t%d: %s" % (num_sets, a_set[0].kind)
		
		print "\t0. Cancel"
		print "\nTo which color set do you want to add a house?"
		
		selection = None
		while True:
			try:
				selection = int(raw_input(": "))
				if selection in range(0, num_sets + 1):
					break
			except ValueError:
				pass

			print "Try again, it looks like you mistyped."

		if selection == 0:
			return False

		set_color = full_sets[selection - 1][0].kind
		self = ColoredProperty(self.name, self.value, set_color)
		full_sets[selection - 1].append(self)
		log.add("You played %s on the %s set." % (self.name, set_color), player)
		return True

	def hotel(self, player):
		full_sets = player.get_full_sets()
		to_remove = []

		for a_set in full_sets:
			has_house = False

			for card in a_set:
				if card.name == "Hotel":
					to_remove.append(a_set)
					break

				if card.name == "House":
					has_house = True

			if not has_house:
				to_remove.append(a_set)

			if not isinstance(a_set[0], (ColoredProperty, WildProperty)):
				to_remove.append(a_set)

		full_sets = [a_set for a_set in full_sets if a_set not in to_remove]	
		if not full_sets:
			print "\nYou can't play %s now!" % self.name
			return False	
		
		num_sets = 0
		for a_set in full_sets:
			num_sets += 1
			print "\t%d: %s" % (num_sets, a_set[0].kind)
		
		print "\t0. Cancel"
		print "\nTo which color set do you want to add a hotel?"
		
		selection = None
		while True:
			try:
				selection = int(raw_input(": "))
				if selection in range(0, num_sets + 1):
					break
			except ValueError:
				pass

			print "Try again, it looks like you mistyped."

		if selection == 0:
			return False

		set_color = full_sets[selection - 1][0].kind
		self = ColoredProperty(self.name, self.value, set_color)
		full_sets[selection - 1].append(self)
		log.add("You played %s on the %s set." % (self.name, set_color), player)
		return True

	def pass_go(self, player):
		deck.draw(player, 2)
		log.add("You played %s and drew 2 cards." % self.name, player)
		discards.append(self)
		return True


class Rent(Action):

	def __init__(self, name, value, kinds):
		super(Rent, self).__init__(name, value)
		self.kinds = kinds
		self.kind = self.kinds[0]

	def play(self, player):
		already_banked = Action.play(self, player)

		if already_banked:
			return True

		available_sets = []

		for group in player.properties:
			if group[0].kind in self.kinds:
				available_sets.append(group)

		if not available_sets:
			print "\nYou can't play %s now!" % self.name
			return False

		num_sets = 0
		rates = []
		for group in available_sets:
			num_sets += 1
			num_buildings = len(group) - group[0].full_size()

			if num_buildings <= 0:
				rates.append(group[0].rents_for(len(group) - 1))
				print "\t%d: %s (%d properties) - $%dM" % (
					num_sets, group[0].kind, len(group), rates[num_sets - 1])
			else:
				rate = group[0].rents_for(group[0].full_size() - 1)
				if num_buildings == 1:
					rates.append(rate + 3)
					print "\t%d: %s (%d properties + House) - $%dM" % (
						num_sets, group[0].kind, group[0].full_size(), rates[num_sets - 1])
				if num_buildings == 2:
					rates.append(rate + 7)
					print "\t%d: %s (%d properties + House + Hotel) - $%dM" % (
						num_sets, group[0].kind, group[0].full_size(), rates[num_sets - 1])

		print "\t0. Cancel"
		print "\nOn which set would you like to charge rent?"

		selection = None
		while True:
			try:
				selection = int(raw_input(": "))
				if selection in range(0, num_sets + 1):
					break
			except ValueError:
				pass

			print "Try again, it looks like you mistyped."

		if selection == 0:
			return False

		cards_paid = []
		lines_back = 1

		if len(self.kinds) == 10: # indicating an Any Rent card
			for other in players:
				if other is not player and other.has_assets():
					print "\nCharge %s rent of $%dM?" % (
						other.name, rates[selection - 1])
					print "\t1. Yes."
					print "\t0. No."
					selection_two = raw_input(": ")

					while True:
						if selection_two == '1':
							log.add("You played %s." % self.name, player)

							while player.double_the_rent():
								log.add("You played Double the Rent.", player)
								rates[selection - 1] = rates[selection - 1] * 2
								lines_back += 1

							log.prompt(other, log.lines - lines_back)

							if other.just_say_no(player, "$%dM" % rates[selection - 1]):
								log.add("You played Just Say No, blocking %s's %s." % (
									player.name, self.name), other)
								lines_back += 1
							else:
								cards_paid = other.pay(rates[selection - 1], player)
								for card in cards_paid:
									log.add("You paid %s." % card.name, other)
									lines_back += 1

							log.prompt(player, log.lines - lines_back + 1)
							player.receive(cards_paid)
							discards.append(self)
							return True
						elif selection_two == '0':
							break
						else:
							print "Try again, it looks like you mistyped."
							selection = raw_input(": ")

			print "\nYou can't play %s now!" % self.name
			return False
		else:
			log.add("You played %s." % self.name, player)

			for other in players:
				if other is not player and other.has_assets():
					log.prompt(other, log.lines - lines_back)
					if other.just_say_no(player, "$%dM" % rates[selection - 1]):
						log.add("You played Just Say No, blocking %s's %s." % (
							player.name, self.name), other)
						lines_back += 1
					else:
						new_cards = other.pay(rates[selection - 1], player)
						for card in new_cards:
							log.add("%s paid %s." % (
								other.name, card.name), other)
							lines_back += 1

						cards_paid.extend(new_cards)

			if not cards_paid:
				log.remove()
				print "\nYou can't play %s now!" % self.name
				return False

			log.prompt(player, log.lines - lines_back + 1)
			player.receive(cards_paid)
			discards.append(self)
			return True


class Money(Card):

	def __init__(self, name, value):
		super(Money, self).__init__(name, value)

	def __dir__(self):
		return ['name', 'value']

	def play(self, player):
		player.bank.append(self)
		player.bank_value += self.value

		if "$" not in self.name:
			log.add("You banked %s ($%sM)."
				% (self.name, self.value), player)
		else:
			log.add("You banked %s." % self.name, player)
		return True


deck = Deck()
discards = []
