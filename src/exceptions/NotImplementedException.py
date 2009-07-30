from utaka.src.exceptions.UtakaException import UtakaException

class NotImplementedException(UtakaException):
	def __init__(self, args):
		UtakaException.__init__(self, args)