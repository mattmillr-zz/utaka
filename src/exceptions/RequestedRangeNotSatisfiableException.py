from utaka.src.exceptions.UtakaException import UtakaException

class RequestedRangeNotSatisfiableException(UtakaException):
	def __init__(self, args):
		UtakaException.__init__(self, args, 416)