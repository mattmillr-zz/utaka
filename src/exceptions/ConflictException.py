from utaka.src.exceptions.UtakaException import UtakaException

class ConflictException(UtakaException):
	def __init__(self, args):
		UtakaException.__init__(self, args, 409)
		
class BucketAlreadyOwnedByYouException(ConflictException):
	def __init__(self, bucket):
		ConflictException.__init__(self,
			{'Code' : 'BucketAlreadyOwnedByYou',
			 'Description' : 'You already own bucket',
			 'Bucket' : bucket})