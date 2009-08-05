from utaka.src.exceptions.UtakaException import UtakaException

class NotModifiedException(UtakaException):
	def __init__(self):
		UtakaException.__init__(self, {}, 304)