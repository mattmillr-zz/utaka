

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