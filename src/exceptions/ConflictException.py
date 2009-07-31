from utaka.src.exceptions.UtakaException import UtakaException

class ConflictException(UtakaException):
	def __init__(self, args):
		UtakaException.__init__(self, args, 409)