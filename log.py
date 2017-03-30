class GameLog(object):

	def __init__(self):
		self.prev_lines = 0
		self.lines = 0
		self.history = []

	def add(self, string, player):
		print string
		string = string.replace("You", player.name)
		self.history.append(string)
		self.lines += 1
		
	def show(self, start=0):
		for line in range(start, self.lines):
			print line, self.history[line]

log = GameLog()