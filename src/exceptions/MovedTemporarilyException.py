from utaka.src.exceptions.UtakaException import UtakaException

class MovedTemporarilyException(UtakaException):
	def __init__(self, args):
		UtakaException.__init__(self, args)