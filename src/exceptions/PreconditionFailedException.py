from utaka.src.exceptions.UtakaException import UtakaException

class PreconditionFailedException(UtakaException):
	def __init__(self, condition):
		UtakaException.__init__(self,
			{'Message' : 'At least one of the pre-conditions you specified did not hold',
			 'Condition' : str(condition),
			 'Code' : 'PreconditionFailed'}, 412)

class IfUnmodifiedSinceFailedException(PreconditionFailedException):
	def __init__(self):
		PreconditionFailedException.__init__(self, 'If-Unmodified-Since')
		
class IfMatchFailedException(PreconditionFailedException):
	def __init__(self):
		PreconditionFailedException.__init__(self, 'If-Match')