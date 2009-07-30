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

from mod_python import apache
from utaka.src.rest.UtakaRequest import UtakaRequest
from utaka.src.exceptions import *
#message handler

def handler(req):

	try:
		utakaRequest = UtakaRequest(req)

		if utakaRequest.key:
			from utaka.src.rest.UtakaObject import UtakaObject
			restResource = UtakaObject(utakaRequest)
		elif utakaRequest.bucket:
			from utaka.src.rest.UtakaBucket import UtakaBucket
			restResource = UtakaBucket(utakaRequest)
		else:
			from utaka.src.rest.UtakaService import UtakaService
			restResource = UtakaService(utakaRequest)

		restResource.handleRequest()

	except UtakaException.UtakaException, e:
		if isinstance(e, MovedPermanentlyException.MovedPermanentlyException):
			req.status = 301
		elif isinstance(e, MovedTemporarilyException.MovedTemporarilyException):
			req.status = 307
		if isinstance(e, BadRequestException.BadRequestException):
			req.status = 400
		elif isinstance(e, ForbiddenException.ForbiddenException):
			req.status = 403
		elif isinstance(e, NotFoundException.NotFoundException):
			req.status = 404
		elif isinstance(e, MethodNotAllowedException.MethodNotAllowedException):
			req.status = 405
		elif isinstance(e, ConflictException.ConflictException):
			req.status = 409
		elif isinstance(e, LengthRequiredException.LengthRequiredException):
			req.status = 411
		elif isinstance(e, PreconditionFailException.PreconditionFailException):
			req.status = 412
		elif isinstance(e, RequestedRangeNotSatisfiableException.RequestedRangeNotSatisfiableException):
			req.status = 416
		elif isinstance(e, InternalErrorException.InternalErrorException):
			req.status = 500
		elif isinstance(e, NotImplementedException.NotImplementedException):
			req.status = 501
		elif isinstance(e, ServiceUnavailableException.ServiceUnavailableException):
			req.status = 503
		#print out error xml

	else:
		utakaRequest.send()

	return apache.OK