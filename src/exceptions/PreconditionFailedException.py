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

PreconditionFailedException and subclasses, all subclass UtakaException with an httpStatus of 412
@author: Andrew
'''
from utaka.src.exceptions.UtakaException import UtakaException

class PreconditionFailedException(UtakaException):
	def __init__(self, condition):
		UtakaException.__init__(self,
			{'Message' : 'At least one of the pre-conditions you specified did not hold',
			 'Condition' : str(condition),
			 'Code' : 'PreconditionFailed'}, 412)

class IfUnmodifiedSinceFailedException(PreconditionFailedException):
	def __init__(self):
		PreconditionFailedException.__init__(self, 'If-Unmodified-Since')
		
class IfMatchFailedException(PreconditionFailedException):
	def __init__(self):
		PreconditionFailedException.__init__(self, 'If-Match')