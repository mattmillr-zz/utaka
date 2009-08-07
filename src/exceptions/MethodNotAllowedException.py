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

MethodNotAllowedException and subclasses, all subclass UtakaException with an httpStatus of 405
@author: Andrew
'''
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