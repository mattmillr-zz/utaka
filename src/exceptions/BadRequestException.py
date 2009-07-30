
from utaka/src/exceptions/UtakaException import UtakaException

#400
class BadRequestException(UtakaException):
	def __init__(self, args):
		UtakaException.__init__(self, args)

class AmbiguousGrantByEmailAddress(BadRequestException):
	def __init__(self):
		BadRequestException.__init__(self,
			{'Message' : 'The e-mail address you provided is associated with more than one account.',
			 'Code' : 'BadRequest'})
		
class BadDigestException(BadRequestException):
	def __init__(self, expectedDigest, calculatedDigest):
		BadRequestException.__init__(self, 
			{'Message' : 'The Content-MD5 you specified did not match what we received',
			 'ExpectedDigest' : expectedDigest,
			 'CalculatedDigest' : calculatedDigest,
			 'Code' : 'BadDigest'})

class CredentialsNotSupported(BadRequestException):
	def __init__(self):
		BadRequestException.__init__(self,
			{'Message' : 'This request does not support credentials',
			 'Code' : 'CredentialsNotSupported'})
		
class EntityTooSmallException(BadRequestException):
	def __init__(self):
		BadRequestException.__init__(self,
			{'Message' : 'Your proposed upload is smaller than the minimum allowed object size',
			 'Code' : 'EntityTooSmall'})
		
class EntityTooLargeException(BadRequestException):
	def __init__(self):
		BadRequestException.__init__(self,
			{'Message' : 'Your proposed upload exceeds the maximum allowed object size',
			 'Code' : 'EntityTooLarge'})
		
class ExpiredTokenException(BadRequestException):
	def __init__(self):
		BadRequestException.__init__(self,
			{'Message' : 'The provided token has expired.',
			 'Code' : 'ExpiredToken'})

class IncompleteBodyException(BadRequestException):
	def __init__(self):
		BadRequestException.__init__(self,
			{'Message' : 'You did not provide the number of bytes specified by the Content-Length HTTP Header',
			 'Code' : 'IncompleteBody'})
		
class IncorrectNumberOfFilesInPostRequestException(BadRequestException):
	def __init__(self):
		BadRequestException.__init__(self,
			{'Message' : 'POST requires exactly one file upload per request',
			 'Code' : 'IncorrectNumberOfFilesInPostRequest'})
		
class InlineDataTooLargeException(BadRequestException):
	def __init__(self):
		BadRequestException.__init__(self,
			{'Message' : 'Inline data exceeds the maximum allowed size',
			 'Code' : 'InlineDataTooLarge'})

class InvalidArgumentException(BadRequestException):
	def __init__(self, argumentValue, argumentName):
		BadRequestException.__init__(self,
			{'Message' : 'Invalid Argument',
			 'Code' : 'InvalidArgument',
			 'ArgumentValue' : argumentValue,
			 'ArgumentName' : argumentName})

class InvalidBucketNameException(BadRequestException):
	def __init__(self, bucketName):
		BadRequestException.__init__(self,
			{'Message' : 'The specified bucket is not valid',
			 'Code' : 'InvalidBucketName',
			 'BucketName' : bucketName})

class InvalidDigestException(BadRequestException):
	def __init__(self, contentMD5):
		BadRequestException.__init__(self,
			{'Message' : 'The Content-MD5 you specified is not valid',
			 'Code' : 'InvalidDigest',
			 'Content-MD5' : contentMD5})

class InvalidLocationConstraintException(BadRequestException):
	def __init__(self):
		BadRequestException.__init__(self,
			{'Message' : 'The specified location constraint is not valid',
			 'Code' : 'InvalidLocationConstraint'})
		
class InvalidPolicyDocumentException(BadRequestException):
	def __init__(self):
		BadRequestException.__init__(self,
			{'Message' : 'The content of the form does not meet the conditions specified in the policy document',
			 'Code' : 'InvalidPolicyDocument'})
		
class InvalidSOAPRequestException(BadRequestException):
	def __init__(self):
		BadRequestException.__init__(self,
			{'Message' : 'The SOAP request body is invalid',
			 'Code' : 'InvalidSOAPRequest'})
		
class InvalidStorageClassException(BadRequestException):
	def __init__(self):
		BadRequestException.__init__(self,
			{'Message' : 'The storage class you specified is not valid',
			 'Code' : 'InvalidStorageClass'})
		
class InvalidTargetBucketForLoggingException(BadRequestException):
	def __init__(self, targetBucket):
		BadRequestException.__init__(self,
			{'Message' : 'The target bucket for logging does not exist, is not owned by you, or does not have the appropriate grants for the log-delivery group.',
			 'Code' : 'InvalidTargetBucketForLogging',
			 'TargetBucket' : targetBucket})
		
class InvalidTokenException(BadRequestException):
	def __init__(self):
		BadRequestException.__init__(self,
			{'Message' : 'The provided token is malformed or otherwise invalid',
			 'Code' : 'InvalidTokenException'})

class InvalidURIException(BadRequestException):
	def __init__(self):
		BadRequestException.__init__(self,
			{'Message' : "Couldn't parse the specified URI.",
			 'Code' : 'InvalidURI'})
		
class KeyTooLongException(BadRequestException):
	def __init__(self, args):
		BadRequestException.__init__(self,
			{'Message' : 'Your key is too long',
			 'Code' : 'KeyTooLong'})
		
class MalformedACLErrorException(BadRequestException):
	def __init__(self):
		BadRequestException.__init__(self,
			{'Message' :'The XML you provided was not well-formed or did not validate against our published schema',
			 'Code' : 'MalformedACL'})
		
class MalformedPOSTRequestException(BadRequestException):
	def __init__(self):
		BadRequestException.__init__(self,
			{'Message' : 'The body of your POST request is not well-formed multipart/form-data.',
			 'Code' : 'MalformedPOSTRequest'})
		
class MalformedXMLException(BadRequestException):
	def __init__(self):
		BadRequestException.__init__(self,
			{'Message' : 'The XML you provided was not well-formed or did not validate against our published schema',
			 'Code' : 'MalformedXML'})
		
class MaxMessageLengthExceededException(BadRequestException):
	def __init__(self):
		BadRequestException.__init__(self,
			{'Message' : 'Your request was too big',
			 'Code' : 'MaxMessageLengthExceeded'})
		
class MaxPostPreDataLengthExceededErrorException(BadRequestException):
	def __init__(self):
		BadRequestException.__init__(self,
			{'Message' : 'Your POST request fields preceding the upload file were too large.',
			 'Code' : 'MaxPostPreDataLengthExceededError'})
		
class MetadataTooLargeException(BadRequestException):
	def __init__(self):
		BadRequestException.__init__(self,
			{'Message' : 'Your metadata eaders exceed the maximum allowed metadata size.',
			 'Code' : 'MetadataTooLarge'})
		
class MissingRequestBodyErrorException(BadRequestException):
	def __init__(self):
		BadRequestException.__init__(self,
			{'Message' : 'Request body is empty',
			 'Code' : 'MissingRequestBodyError'})
		
class MissingSecurityElementException(BadRequestException):
	def __init__(self):
		BadRequestException.__init__(self,
			{'Message' : 'The SOAP 1.1 request is missing a security element',
			 'Code' : 'MissingSecurityElement'})
			 
class MissingSecurityHeaderException(BadRequestException):
	def __init__(self):
		BadRequestException.__init__(self,
			{'Message' : 'Your request was missing a required header',
			 'Code' : 'MissingSecurityHeader'})
		
class NoLoggingStatusForKeyException(BadRequestException):
	def __init__(self):
		BadRequestException.__init__(self,
			{'Message' : 'There is no such thing as a logging status sub-resource for a key',
			 'Code' : 'NoLoggingStatusForKey'})
		
class RequestIsNotMultiPartContentException(BadRequestException):
	def __init__(self):
		BadRequestException.__init__(self,
			{'Message' : 'Bucket POST must be of the enclosure-type multipart/form-data.',
			 'Code' : 'RequestIsNotMultiPartContent'})
		
class RequestTimeoutException(BadRequestException):
	def __init__(self):
		BadRequestException.__init__(self,
			{'Message' : 'Your socket connection to the server was not read from or written to within the timeout period',
			 'Code' : 'RequestTimeout'})
		
class RequestTorrentOfBucketErrorException(BadRequestException):
	def __init__(self):
		BadRequestException.__init__(self,
			{'Message' : 'Requesting the torrent file of a bucket is not permitted',
			 'Code' : 'RequestTorrentOfBucketError'})
		
class TokenRefreshRequiredException(BadRequestException):
	def __init__(self):
		BadRequestException.__init__(self,
			{'Message' : 'The provided token must be refreshed',
			 'Code' : 'TokenRefreshRequired'})
		
class TooManyBucketsException(BadRequestException):
	def __init__(self):
		BadRequestException.__init__(self,
			{'Message' : 'You have attempted to create more buckets than allowed',
			 'Code' : 'TooManyBuckets'})
		
class UnexpectedContentException(BadRequestException):
	def __init__(self):
		BadRequestException.__init__(self,
			{'Message' : 'This request does not support content',
			 'Code' : 'UnexpectedContent'})
		
class UnresolvableGrantByEmailAddressException(BadRequestException):
	def __init__(self, email):
		BadRequestException.__init__(self,
			{'Message' : 'The e-mail address you provided does not match any account on record',
			 'Code' : 'UnresolvableGrantByEmailAddress',
			 'E-mail' : email})
		
class UserKeyMustBeSpecifiedException(BadRequestException):
	def __init__(self):
		BadRequestException.__init__(self,
			{'Message' : 'The bucket POST must contain the specified field name. If it is specified, please check the order of the fields.',
			 'Code' : 'UserKeyMustBeSpecified'})