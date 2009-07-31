from utaka.src.exceptions.UtakaException import UtakaException

class NotFoundException(UtakaException):
	def __init__(self, args):
		UtakaException.__init__(self, args, 404)
		
class NoSuchBucketException(NotFoundException):
	def __init__(self, bucket):
		NotFoundException.__init__(self,
			{'Message' : 'The specified bucket does not exist',
			 'Code' : 'NoSuchBucket',
			 'BucketName' : bucket})
			 
class NoSuchKeyException(NotFoundException):
	def __init__(self, bucket, key):
		NotFoundException.__init__(self,
			{'Message' : 'The specified key does not exist',
			 'Code' : 'NoSuchKey',
			 'Key' : key,
			 'BucketName' : bucket})