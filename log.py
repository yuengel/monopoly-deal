import os

class GameLog(object):

	def __init__(self):
		self.prev_lines = 0
		self.lines = 0
		self.history = []
		self.log_file = open("gamelog.txt", "a")

	def add(self, string, player):
		print string
		string = string.replace("You", player.name)
		self.history.append(string)
		
		string = "%d: %s\n" % (self.lines, string)
		self.log_file.write(string)
		self.lines += 1
		
	def show(self, start=0):
		for line in range(start, self.lines):
			print "\t%d: %s" % (line, self.history[line])

	def prompt(self, player, start=0, string=""):
		"""Clears screen and prompts player to begin their turn. 
		Posts game log from int start to end. Also preprints optional string.
		"""

		os.system('cls')
		print string
		self.show(start)
		raw_input("\nIt's your turn now, %s! Hit ENTER to continue." % player.name)
		os.system('cls')			


log = GameLog()