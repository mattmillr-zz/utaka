
class UtakaException(Exception):
	def __init__(self, args, httpStatus=200):
		self.args = args
		self.httpStatus = httpStatus
	def __str__(self):
		return str(httpStatus) + ": " + str(self.args)