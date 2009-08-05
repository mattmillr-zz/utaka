from utaka.src.exceptions.UtakaException import UtakaException
import utaka.src.Config as Config

class ForbiddenException(UtakaException):
	def __init__(self, args):
		UtakaException.__init__(self, args, 403)
		
class AccessDeniedException(ForbiddenException):
	def __init__(self):
		ForbiddenException.__init__(self,
			{'Message' : 'Access Denied',
			 'Code' : 'AccessDenied'})
			 
class SignatureDoesNotMatchException(ForbiddenException):
	def __init__(self, stringToSignBytes, stringToSign, signatureProvided, accessKey):
		accesskeyIdPrefix = str(Config.get('authentication', 'prefix'))
		ForbiddenException.__init__(self,
			{'Message' : 'The request signature we calculated des not match the signature you provided. Check your key and signing method.',
			 'Code' : 'SignatureDoesNotMatch',
			 'StringToSignBytes' : str(stringToSignBytes),
			 'StringToSign' : str(stringToSign),
			 'SignatureProvided' : str(signatureProvided),
			 accesskeyIdPrefix + 'AccessKeyId' : str(accessKey)})
			 
class InvalidAccessKeyIdException(ForbiddenException):
	def __init__(self, accessKey):
		accesskeyIdPrefix = str(Config.get('authentication', 'prefix'))
		ForbiddenException.__init__(self,
			{'Message' : 'The ' + accesskeyIdPrefix + ' Access Key Id you provided does not exist in our records',
			 'Code' : 'InvalidAccessKeyId',
			 accesskeyIdPrefix + 'AccessKey' : str(accessKey)})