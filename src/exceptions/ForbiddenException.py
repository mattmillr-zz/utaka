from utaka/src/exceptions/UtakaException import UtakaException

class ForbiddenException(UtakaException):
	def __init__(self, args):
		UtakaException(self, args)
		
class AccessDeniedException(ForbiddenException):
	def __init__(self):
		NotFoundException(self,
			{'Message' : 'Access Denied',
			 'Code' : 'AccessDenied'})