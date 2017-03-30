import os

class Player(object):

	def __init__(self, name):
		self.name = name
		self.hand = []
		self.properties = []
		self.bank = []
		self.bank_value = 0

	def prompt(self):
		os.system('cls')
		raw_input("It's your turn now, %s! Hit ENTER to continue." % self.name)
		os.system('cls')

	def show_hand(self):
		num_card = 1
		print "\n",
		for card in self.hand:
			print "%d: %s" % (num_card, card.name)
			num_card += 1

	def show_properties(self):
		"""Pretty prints own properties organized by set. Returns number of properties."""

		num_properties = 0
		print "\n",
		for group in self.properties:
			for card in group:
				num_properties += 1
				print "%d: %s" % (num_properties, card.name)
			print "\n",

		return num_properties

	def pay(self, amount, pay_to):
		"""Forces player to pay amount's worth of value to player given in pay_to.
		Returns a list of the cards paid.
		"""

		cards_paid = []
		cards_payable = []

		# Handle empty list, if player has no assets on board
		properties_list = list(self.properties)
		for group in properties_list:
			cards_payable.extend(group)
		cards_payable.extend(self.bank)

		# Show last log move here

		if len(cards_payable) == 0:
			return cards_paid
		else:
			print "Your properties:"
			count = self.show_properties()

			print "Your bank:"
			for bill in self.bank:
				count += 1
				print "%d: %s" % (count, bill.name)
				
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

			card = cards_payable[selection - 1]
			cards_paid.append(card)

			if card in self.properties:
				self.properties.pop(selection - 1)
			elif card in self.bank:
				selection -= len(self.properties)
				self.bank.pop(selection - 1)
				self.bank_value -= card.value

			amount -= card.value

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