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
	debug = True
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
	except Exception, e:
		if not isinstance(e, UtakaException.UtakaException):
			e = InternalErrorException.GeneralErrorException(e)
		req.status = e.httpStatus
		import xml.dom.minidom
		doc = xml.dom.minidom.Document()
		errorEl = doc.createElement("Error")
		for key, val in e.args.iteritems():
			keyEl = doc.createElement(str(key))
			keyEl.appendChild(doc.createTextNode(str(val)))
			errorEl.appendChild(keyEl)
		if debug:
			debugEl = doc.createElement("Debug")
			import traceback
			tracebackEl = doc.createElement("Traceback")
			tracebackEl.appendChild(doc.createTextNode(str(traceback.format_exc())))
			debugEl.appendChild(tracebackEl)
			if 'devArgs' in e.__dict__.keys():
				for key, val in e.devArgs.iteritems():
					keyEl = doc.createElement(str(key))
					keyEl.appendChild(doc.createTextNode(str(val)))
					debugEl.appendChild(keyEl)
			errorEl.appendChild(debugEl)
		doc.appendChild(errorEl)
		req.content_type = 'application/xml'
		errOutput = doc.toxml('utf-8')
		req.content_length = len(errOutput)
		req.write(errOutput)
	else:
		utakaRequest.send()
	return apache.OK