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
	utakaLog = open('/var/www/html/utaka/utakaLog', 'a')
	try:
		utakaLog.write('Client Connected on connection: %s\r\n' % req.connection.id)
	finally:
		utakaLog.close()
	debug = True
	utakaRequest = None
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
		utakaRequest.send()
	except Exception, e:
		dev = bool(utakaRequest and utakaRequest.isUserAdmin)
		if not isinstance(e, UtakaException.UtakaException):
			if dev:
				req.status = 500
				raise
			else:
				e = InternalErrorException.GeneralErrorException(e)
		req.status = e.httpStatus
		e.args['RequestId'] = str(req.connection.id)
		errOutput = e.toxml(True)
		req.content_type = 'application/xml'
		req.content_length = len(errOutput)
		req.write(errOutput)
		utakaLog = open('/var/www/html/utaka/utakaLog', 'a')
		try:
			utakaLog.write('Client Disconnected with error\r\n')
		finally:
			utakaLog.close()
	else:
		utakaLog = open('/var/www/html/utaka/utakaLog', 'a')
		try:
			utakaLog.write('Client Disconnected without error\r\n')
		finally:
			utakaLog.close()
	
	return apache.OK