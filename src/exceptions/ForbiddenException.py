from utaka.src.exceptions.UtakaException import UtakaException

class ForbiddenException(UtakaException):
	def __init__(self, args):
		UtakaException.__init__(self, args, 403)
		
class AccessDeniedException(ForbiddenException):
	def __init__(self):
		ForbiddenException.__init__(self,
			{'Message' : 'Access Denied',
			 'Code' : 'AccessDenied'})