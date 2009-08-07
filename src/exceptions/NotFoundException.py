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

NotFoundException and subclasses, all subclass UtakaException with an httpStatus of 404
@author: Andrew
'''
from utaka.src.exceptions.UtakaException import UtakaException

class NotFoundException(UtakaException):
	def __init__(self, args):
		UtakaException.__init__(self, args, 404)
		
class NoSuchBucketException(NotFoundException):
	def __init__(self, bucket):
		NotFoundException.__init__(self,
			{'Message' : 'The specified bucket does not exist',
			 'Code' : 'NoSuchBucket',
			 'BucketName' : bucket})
			 
class NoSuchKeyException(NotFoundException):
	def __init__(self, bucket, key):
		NotFoundException.__init__(self,
			{'Message' : 'The specified key does not exist',
			 'Code' : 'NoSuchKey',
			 'Key' : key,
			 'BucketName' : bucket})