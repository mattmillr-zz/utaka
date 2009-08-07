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

ConflictException and subclasses, all subclass UtakaException with an httpStatus of 409
@author: Andrew
'''
from utaka.src.exceptions.UtakaException import UtakaException

class ConflictException(UtakaException):
	def __init__(self, args):
		UtakaException.__init__(self, args, 409)
		
class BucketAlreadyOwnedByYouException(ConflictException):
	def __init__(self, bucket):
		ConflictException.__init__(self,
			{'Code' : 'BucketAlreadyOwnedByYou',
			 'Message' : 'You already own bucket',
			 'Bucket' : bucket})
			 
class BucketNotEmptyException(ConflictException):
	def __init__(self, bucket):
		ConflictException.__init__(self,
			{'Code' : 'BucketNotEmpty',
			 'Message' : "Bucket's must be empty to be deleted",
			 'Bucket' : bucket})