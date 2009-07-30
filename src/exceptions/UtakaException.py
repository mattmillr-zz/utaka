
class UtakaException(Exception):
	def __init__(self, args):
		self.args = args
	def __str__(self):
		return str(self.args)