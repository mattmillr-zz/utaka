from utaka.src.exceptions.UtakaException import UtakaException

class InternalErrorException(UtakaException):
	def __init__(self, args):
		UtakaException.__init__(self, args)