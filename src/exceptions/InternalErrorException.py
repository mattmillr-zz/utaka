#Copyright 2009 Humanitarian International Services Group
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

'''
Created July, 2009

InternalErrorException and subclasses, all subclass UtakaException with an httpStatus of 500
	also contain a second dictionary member, devArgs
@author: Andrew
'''
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
