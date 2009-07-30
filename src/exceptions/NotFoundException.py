from utaka/src/exceptions/UtakaException import UtakaException

class NotFoundException(UtakaException):
	def __init__(self, args):
		UtakaException(self, args)
		
class NoSuchBucketException(NotFoundException):
	def __init__(self, bucketName):
		NotFoundException(self,
			{'Message' : 'The specified bucket does not exist',
			 'Code' : 'NoSuchBucket',
			 'BucketName' : bucketName})