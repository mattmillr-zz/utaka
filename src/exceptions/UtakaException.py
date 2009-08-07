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

UtakaException, defaults with an httpStatus of 200
@author: Andrew
'''

class UtakaException(Exception):
	def __init__(self, args, httpStatus=200):
		self.args = args
		self.httpStatus = httpStatus

	def __str__(self):
		return str(httpStatus) + ": " + str(self.args)

	def toxml(self, debug=False):
		import xml.dom.minidom
		doc = xml.dom.minidom.Document()
		errorEl = doc.createElement("Error")
		for key, val in self.args.iteritems():
			keyEl = doc.createElement(str(key))
			keyEl.appendChild(doc.createTextNode(str(val)))
			errorEl.appendChild(keyEl)
		if debug:
			debugEl = doc.createElement("Debug")
			import traceback
			tracebackEl = doc.createElement("Traceback")
			tracebackEl.appendChild(doc.createTextNode(str(traceback.format_exc())))
			debugEl.appendChild(tracebackEl)
			if 'devArgs' in self.__dict__.keys():
				for key, val in self.devArgs.iteritems():
					keyEl = doc.createElement(str(key))
					keyEl.appendChild(doc.createTextNode(str(val)))
					debugEl.appendChild(keyEl)
			errorEl.appendChild(debugEl)
		doc.appendChild(errorEl)
		return doc.toxml('utf-8')