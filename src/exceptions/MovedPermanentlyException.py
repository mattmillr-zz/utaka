from utaka.src.exceptions.UtakaException import UtakaException

class MovedPermanentlyException(UtakaException):
	def __init__(self, args):
		UtakaException.__init__(self, args, 301)