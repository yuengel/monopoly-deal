import os

class Player(object):

	def __init__(self, name):
		self.name = name
		self.hand = []
		self.properties = []
		self.bank = []
		self.bank_value = 0
		self.prev_move = 0

	def show_hand(self):
		num_card = 1
		print "\n",
		for card in self.hand:
			value_string = "$%dM" % card.value
			if card.name == value_string:
				print "\t%d: %s" % (num_card, card.name)
			else:
				print "\t%d: %s - %s" % (num_card, card.name, value_string)
			num_card += 1

	def has_assets(self, the_filter=None):
		"""Returns true if either bank or properties is not empty, filtered
		according to dice given in the_filter. Defaults all properties.
		"""

		if len(self.get_properties(the_filter)) == 0 and len(self.bank) == 0:
			return False
		else:
			return True

	def filter_properties(self, a_filter='all'):
		"""Returns a dict. The keys refer to indices of cards in a list of properties
		that has the selected filter applied. The values refer to the actual indices
		of each card in self.properties. a_filter takes the values 'all', 'no_full_sets',
		'no_buildings', and 'no_any_wilds'.
		"""
		
		index_key = 0
		index_value = 0
		index_dict = {}

		for group in self.properties:
			if a_filter == 'no_full_sets' and len(group) >= group[0].full_size():
				index_value += len(group)
				continue

			for card in group:
				if a_filter == 'no_buildings' and card.name == "House" or card.name == "Hotel":
					index_value += 1
					continue
				if a_filter == 'no_any_wilds' and card.name == "Property Wild: Any":
					index_value += 1
					continue

				index_dict[index_key] = index_value
				index_key += 1
				index_value += 1

		return index_dict

	def get_properties(self, the_filter=None):
		"""Returns a flattened list of player's properties, filtered
		according to dict given in the_filter. Defaults all properties.
		"""
		
		unfiltered_list = [card for group in self.properties for card in group]
		filtered_list = []
		
		if the_filter is not None:
			for value in the_filter.values():
				filtered_list.append(unfiltered_list[value])
		else:
		 	return unfiltered_list

		return filtered_list

	"""def show_properties(self):
		Pretty prints own properties organized by set.
		Returns flattened list of properties.

		num_properties = 0
		for group in self.properties:
			for card in group:
				num_properties += 1
				print "\t%d: %s" % (num_properties, card.name)
			print "\n",

		return [card for group in self.properties for card in group]
	"""

	def reorganize(self):
		"""Allows the player to reorganize their properties."""

		properties_list = self.get_properties()
		num_properties = 0
		if not properties_list:
			print "\nYou don't have anything to move!"
			return

		for card in properties_list:
			num_properties += 1
			print "\t%d: %s" % (num_properties, card.name)
		
		print "\t0. Go back."
		print "Which property would you like to move?"

		selection = None
		while True:
			try:
				selection = int(raw_input(": "))
				if selection in range(0, num_properties + 1):
					break
			except ValueError:
				pass

			print "Try again, it looks like you mistyped."

		if selection == 0:
			return

		property_index = 0
		for group in self.properties:
			for card in group:
				if selection - 1 == property_index:
					group.remove(card) # this is fine because the loop ends before iterating again
					self.properties[:] = [x for x in self.properties if x != []] # Remove empty lists
					card.play(self)
					return
				else:
					property_index += 1

		print "player.reorganize() The card to be reorganized was never found"
				
	def get_full_sets(self):
		"""Returns list only of full sets."""

		full_sets = []

		for group in self.properties:
			try:
				if len(group) >= group[0].full_size():
					full_sets.append(group)
			except IndexError:
				print "Player.get_full_sets() IndexError"

		return full_sets

	def just_say_no(self, string=None):
		"""Returns true if player has Just Say No card and chooses to use it.
		If string is specified, it should be the name of the card targeted."""

		for card in self.hand:
			if card.name == "Just Say No":
				# TODO: Elaborate which action is being taken
				# With Deal Breaker, say which set is being taken
				# With Forced Deal, say which set is being given in exchange
				print "\nDo you want to play your Just Say No card",
				
				if string is not None:
					print "to stop %s from being stolen?" % string
				else:
					print "to stop this action?"

				print "\t1. Yes."
				print "\t0. No."
				selection = raw_input(": ")

				while True:
					if selection == '1':
						 return card.just_say_no(self)
						 # TODO: Allow multiple Just Say Nos to be played in succession
					elif selection == '0':
						return False
					else:
						print "Try again, it looks like you mistyped."
						selection = raw_input(": ")

	def pay_one(self, to_pay):
		"""Forces player to give up a single property. Returns the property."""

		property_index = 0
		to_remove = []
		attached_buildings = []

		for group in self.properties:
			for card in group:
				if property_index == to_pay:
					to_remove.append(card) 
					property_index += 1
					
					for another_card in group:
						if another_card.name == "House" or another_card.name == "Hotel":
							attached_buildings.append(another_card)
				else:
					property_index += 1

			group[:] = [card for card in group if card not in to_remove]
			group[:] = [card for card in group if card not in attached_buildings]		
			self.properties[:] = [x for x in self.properties if x != []] # Remove empty lists

			for card in attached_buildings:
				card.play(self)

			attached_buildings = []

		if not to_remove:
			print "player.pay_one() No card was ever removed"
		else:
			return to_remove[0]

	def pay(self, amount, pay_to):
		"""Forces player to pay amount's worth of value to player given in pay_to.
		Returns a list of the cards paid.
		"""

		cards_paid = []
		no_any_wilds = self.filter_properties('no_any_wilds')

		if not self.has_assets(no_any_wilds):
			return cards_paid
		else:
			print "Your properties:"
			count = 0
			properties_list = self.get_properties(no_any_wilds)
			
			for card in properties_list:
				count += 1
				print "\t%d: %s (%s) - $%dM" % (count, card.name, card.kind, card.value)

			print "\nYour bank:"
			for bill in self.bank:
				count += 1
				if "$" in bill.name:
					print "\t%d: %s" % (count, bill.name)
				else:
					print "\t%d: %s - $%sM" % (count, bill.name, bill.value)
				
			print "\nWhich card would you like to pay to %s?" % pay_to.name

			selection = None
			while True:
				try:
					selection = int(raw_input(": "))
					if selection in range(1, count + 1):
						break
				except ValueError:
					pass
						
				print "Try again, it looks like you mistyped."

			if selection in range(1, len(properties_list) + 1):
				new_card = self.pay_one(selection - 1)
				amount -= new_card.value
				cards_paid.append(new_card)
			else:
				selection -= len(properties_list)
				card = self.bank.pop(selection - 1)
				cards_paid.append(card)
				amount -= card.value
				self.bank_value -= card.value

			if amount > 0:
				new_card = self.pay(amount, pay_to)
				cards_paid.extend(new_card)

			return cards_paid

	def receive(self, cards):
		"""Takes a list of cards. Plays all cards received."""
		for card in cards:
			card.play(self)
		print "\n",


players = []