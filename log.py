import os

class GameLog(object):

	def __init__(self):
		self.prev_lines = 0
		self.lines = 0
		self.buffer_lines = 0
		self.history = []
		self.buffer = []
		self.log_file = open("game-log.txt", "w")

	def add(self, string, player):

		string = string.replace("You", player.name)
		self.history.append(string)
		
		string = "%d: %s\n" % (self.lines, string)
		self.log_file.write(string)
		self.lines += 1

	def add_to_buffer(self, string, player):
		"""Same as self.add() except prints to screen and does not write to history/log file."""

		print string
		string = string.replace("You", player.name)
		self.buffer.append(string)
		self.buffer_lines += 1

	def write_buffer(self, player):
		for line in self.buffer:
			log.add(line, player)
		
	def clear_buffer(self):
		self.buffer[:] = []
		self.buffer_lines = 0

	def remove(self):
		self.history.pop()
		self.lines -= 1
		for line in self.history:
			self.log_file.write(line)
		
	def show(self, start=0):
		for line in range(start, self.lines):
			print "%d: %s" % (line, self.history[line])

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
