from utaka.src.exceptions.UtakaException import UtakaException

class NotImplementedException(UtakaException):
	def __init__(self, args):
		UtakaException.__init__(self, args, 501)
		
class GetLoggingNotImplementedException(NotImplementedException):
	def __init__(self):
		NotImplementedException.__init__(self,
			{'Code' : 'GetLoggingNotImplemented',
			 'Message' : 'Getting and Setting of bucket logging is not implemented. Bucket logs may be found in each bucket under keys beginning with __utaka__<Bucket>__logs/'})