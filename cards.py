import json

class Card(object):

	def __init__(self, name, value):
		self.name = name
		self.value = value

	def play(self):
		pass

class Property(Card):

	def __init__(self, name, value, kind):
		super(Property, self).__init__(name, value)
		self.kind = kind


class ColoredProperty(Property):

	def __init__(self, name, value, kind):
		super(ColoredProperty, self).__init__(name, value, kind)

	def __dir__(self):
		return ['name', 'value', 'kind']


class OtherProperty(Property):

	def __init__(self, name, value, kind):
		super(OtherProperty, self).__init__(name, value, kind)

	def __dir__(self):
		return ['name', 'value', 'kind']


class WildProperty(Property):

	def __init__(self, name, value, kind):
		super(WildProperty, self).__init__(name, value, kind)

	def __dir__(self):
		return ['name', 'value', 'kind']


class Action(Card):

	def __init__(self, name, value):
		super(Action, self).__init__(name, value)
		self.kind = self.name

	def __dir__(self):
		return ['name', 'value']


class Money(Card):

	def __init__(self, name, value):
		super(Money, self).__init__(name, value)

	def __dir__(self):
		return ['name', 'value']



def assemble_deck():
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