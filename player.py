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
			print "\t%d: %s" % (num_card, card.name)
			num_card += 1

	def has_assets(self):
		"""Returns true if either bank or properties is not empty."""

		if len(self.properties) == 0 and len(self.bank) == 0:
			return False
		else:
			return True

	def show_properties(self):
		"""Pretty prints own properties organized by set.
		Returns flattened list of properties."""

		num_properties = 0
		for group in self.properties:
			for card in group:
				num_properties += 1
				print "\t%d: %s" % (num_properties, card.name),
			print "\n",

		return [card for group in self.properties for card in group]

	def reorganize(self):
		"""Allows the player to reorganize their properties."""

		properties_list = self.show_properties()

		if not properties_list:
			print "You don't have anything to move!"
			return
			
		num_properties = len(properties_list)
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

		card_name = properties_list[selection - 1].name
		the_card = None
		for group in self.properties:
			for card in group:
				if card.name == card_name:
					the_card = card
					group.remove(card)

		self.properties[:] = [x for x in self.properties if x != []] # Remove empty lists
		the_card.play(self)

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

	def pay_full_set(self, to_pay):
		"""Forces player to give up a full set of cards. Returns the set."""

		# Ask if player wants to play Just Say No here

		self.properties.remove(to_pay)
		return to_pay

	def pay(self, amount, pay_to):
		"""Forces player to pay amount's worth of value to player given in pay_to.
		Returns a list of the cards paid.
		"""

		cards_paid = []
		
		if not self.has_assets():
			return cards_paid
		else:
			print "Your properties:"
			properties_list = self.show_properties()
			count = len(properties_list)

			print "\nYour bank:"
			for bill in self.bank:
				count += 1

				print "\t%d: %s" % (count, bill.name),
				
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
				card_name = properties_list[selection - 1].name

				for group in self.properties:
					for card in group:
						if card.name == card_name:
							cards_paid.append(card)
							amount -= card.value
							group.remove(card)
							
				self.properties[:] = [x for x in self.properties if x != []] # Remove empty lists

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
		print "\nYou received: "
		for card in cards:
			print card.name

		for card in cards:
			card.play(self)


players = []