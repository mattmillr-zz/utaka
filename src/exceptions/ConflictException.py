from utaka.src.exceptions.UtakaException import UtakaException

class ConflictException(UtakaException):
	def __init__(self, args):
		UtakaException.__init__(self, args, 409)
		
class BucketAlreadyOwnedByYouException(ConflictException):
	def __init__(self, bucket):
		ConflictException.__init__(self,
			{'Code' : 'BucketAlreadyOwnedByYou',
			 'Message' : 'You already own bucket',
			 'Bucket' : bucket})
			 
class BucketNotEmptyException(ConflictException):
	def __init__(self, bucket):
		ConflictException.__init__(self,
			{'Code' : 'BucketNotEmpty',
			 'Message' : "Bucket's must be empty to be deleted",
			 'Bucket' : bucket})