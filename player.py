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
		"""Pretty prints own properties organized by set. Returns number of properties."""

		num_properties = 0
		for group in self.properties:
			for card in group:
				num_properties += 1
				print "\t%d: %s" % (num_properties, card.name),
			print "\n",

		return num_properties

	def pay(self, amount, pay_to):
		"""Forces player to pay amount's worth of value to player given in pay_to.
		Returns a list of the cards paid.
		"""

		cards_paid = []
		properties_list = []

		for group in self.properties:
			properties_list.extend(group)

		if not self.has_assets():
			return cards_paid
		else:
			print "Your properties:"
			count = self.show_properties()

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