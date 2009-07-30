
class UtakaException(Exception):
	def __init__(self, args):
		self.args = args
	def __str__(self):
		return str(self.args)

#400
class BadRequestException(UtakaException):
	def __init__(self, args):
		UtakaException.__init__(self, args)

#403
class ForbiddenException(UtakaException):
	def __init__(self, args):
		UtakaException.__init__(self, args)

#404
class NotFoundException(UtakaException):
	def __init__(self, args):
		UtakaException.__init__(self, args)

#405
class MethodNotAllowedException(UtakaException):
	def __init__(self):
		UtakaException.__init__(self, {'msg' : 'The specified method is not allowed against this resource.'})

#409
class ConflictException(UtakaException):
	def __init__(self, args):
		UtakaException.__init__(self, args)


#411
class LengthRequiredException(UtakaException):
	def __init__(self):
		UtakaException.__init__(self, {'msg' : 'You must provide the Content-Length HTTP header.' })

#416
class RequestedRangeNotSatisfiableException(UtakaException):
	def __init__(self):
		UtakaException.__init__(self, {'msg' : 'The requested range cannot be satisfied'})


#500
class InternalServerException(UtakaException):
	def __init__(self):
		UtakaException.__init__(self, {'msg' : 'We encountered an internal error. Please try again.'})




#501
class NotImplementedException(UtakaException):
	def __init__(self, args):
		UtakaException.__init__(self, args)





















class BadDigestException(BadRequestException):
	def __init__(self, expectedDigest, calculatedDigest):
		BadRequestException.__init__(self, {'msg' : 'The Content-MD5 you specified did not match what we received', 'ExpectedDigest' : expectedDigest, 'CalculatedDigest' : calculatedDigest})

class BucketAlreadyExistsException(ForbiddenException):
	UtakaException.__init__(self, {'msg': 'The named bucket you tried to create already exists', 'BucketName' : bucketName})

class InvalidArgumentException(BadRequestException):
	def __init__(self, argumentValue, argumentName):
		BadRequestException.__init__(self, {'msg' : 'Invalid Argument', 'ArgumentValue' : argumentValue, 'ArgumentName' : argumentName })

class InvalidAccessKeyIdException(BadRequestException):
	def __init__(self, accessKeyId):
		BadRequestException.__init__(self, {'msg' : 'Invalid AccessKeyId', 'AccessKeyId' : accessKeyId })

class InvalidDigestException(BadRequestException):
	def __init__(self):
		BadRequestException.__init__(self, {'msg' : 'The Content-MD5 you specified is not valid'})

class EntityTooLargeException(BadRequestException):
	def __init__(self):
		BadRequestException.__init__(self, {'msg' : 'Your proposed upload exceeds the maximum allowed object size' })

class