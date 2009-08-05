from utaka.src.exceptions.UtakaException import UtakaException

class MethodNotAllowedException(UtakaException):
	def __init__(self, resourceType, method, allowedMethod):
		UtakaException.__init__(self,
			{'Code' : 'MethodNotAllowed',
			 'Message' : 'The specified method is not allowed against this resource',
			 'ResourceType' : str(resourceType).upper(),
			 'Method' : str(method).upper(),
			 'AllowedMethod' : str(allowedMethod).upper()}, 405)

class BucketMethodNotAllowedException(MethodNotAllowedException):
	def __init__(self, method):
		MethodNotAllowedException.__init__(self, 'BUCKET', method, 'PUT')

class ObjectMethodNotAllowedException(MethodNotAllowedException):
	def __init__(self, method):
		MethodNotAllowedException.__init__(self, 'OBJECT', method, 'PUT')

class ServiceMethodNotAllowedException(MethodNotAllowedException):
	def __init__(self, method):
		MethodNotAllowedException.__init__(self, 'SERVICE', method, 'GET')
		
class ACLMethodNotAllowedException(MethodNotAllowedException):
	def __init__(self, method):
		MethodNotAllowedException.__init__(self, 'ACL', method, 'PUT')

class LoggingStatusMethodNotAllowedException(MethodNotAllowedException):
	def __init__(self, method):
		MethodNotAllowedException.__init__(self, 'LOGGING_STATUS', method, 'PUT')