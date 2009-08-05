from utaka.src.exceptions.UtakaException import UtakaException
#from MySQLdb import DatabaseError

class InternalErrorException(UtakaException):
	def __init__(self, devArgs):
		self.devArgs = devArgs
		UtakaException.__init__(self,
			{'Message' : 'We encountered an internal error. Please try again.',
			 'Code' : 'InternalError'}, 500)

class BadArgumentException(InternalErrorException):
	def __init__(self, argName, argVal, msg):
		InternalErrorException.__init__(self,
			{'Code' : 'BadArgumentError',
			 'ArgumentName' : str(argName),
			 'ArgumentValue' : str(argVal),
			 'Message' : str(msg)})

class ConfigErrorException(InternalErrorException):
	def __init__(self, configError, configFile):
		InternalErrorException.__init__(self,
			{'Code' : 'ConfigError',
			 'Class' : str(configError.__class__),
			 'Message' : str(configError),
			 'ConfigFile' : str(configFile)})

class DatabaseErrorException(InternalErrorException):
	def __init__(self, databaseError):
		InternalErrorException.__init__(self,
			{'Code' : 'DatabaseError',
			 'Class' : str(databaseError.__class__),
			 'Message' : str(databaseError),
			 'DbErrCode' : str(databaseError.args[0]),
			 'DbErrDetails' : str(databaseError.args[1])})
			 
class DatabaseIntegrityErrorException(InternalErrorException):
	def __init__(self, dbIntegrityError):
		InternalErrorException.__init__(self,
			{'Code' : 'DatabaseIntegrityError',
			 'Class' : dbIntegrityError.__class__,
			 'Message' : dbIntegrityError})

class GeneralErrorException(InternalErrorException):
	def __init__(self, exception):
		InternalErrorException.__init__(self,
			{'Code' : 'GeneralError',
			 'Class' : str(exception.__class__),
			 'Message' : str(exception)})
			 
class HashfieldCollisionErrorException(InternalErrorException):
	def __init__(self, hashfield):
		InternalErrorException.__init__(self,
			{'Code' : 'HashfieldCollisionError',
			 'Hashfield' : str(hashfield),
			 'Message' : 'A unique hashfield was not found.'})

class KeyCollisionErrorException(InternalErrorException):
	def __init__(self):
		InternalErrorException.__init__(self,
			{'Code' : 'KeyCollisionError',
			 'Message' : 'A unique accesskey and secretkey could not be found.'})
