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

ForbddenException and subclasses, all subclass UtakaException with an httpStatus of 403
@author: Andrew
'''
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