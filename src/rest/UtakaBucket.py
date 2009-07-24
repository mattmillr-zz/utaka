'''
Created on Jul 21, 2009

@author: Andrew
'''




from mod_python import apache
import xml.dom.minidom

class UtakaBucket:

	def __init__(self, utakaReq):
		self.utakaReq = utakaReq


	def handleRequest(self):

		if 'acl' in self.utakaReq.subresources:
			if self.utakaReq.req.method == 'GET':
				operation = __getAclOperation()
			elif self.utakaReq.req.method == 'PUT':
				operation = __putAclOperation()
		elif 'logging' in self.utakaReq.subresources:
			if self.utakaReq.req.method == 'GET':
				operation = __getLoggingOperation()
			elif self.utakaReq.req.method == 'PUT':
				operation = __putLoggingOperation()
		elif self.utakaReq.req.method == 'GET':
			operation = __getOperation()
		elif self.utakaReq.req.method == 'PUT':
			operation = __putOperation()
		elif self.utakaReq.req.method == 'DELETE':
			operation = __deleteOperation()
		elif self.utakaReq.req.method == 'POST':
			operation = __postOperation()
		elif self.utakaReq.req.method == 'COPY':
			operation = __copyOperation()

		return operation()
				#RETURN XML, SET HEADERS
			elif self.utakaReq.method == 'PUT':
				res = setBucket(bucket = self.utakaReq.bucket, user = self.utakaReq.user)
				#SET HEADERS
			elif self.utakaReq.req.method == 'DELETE':
				res = destroyBucket(bucket=self.utakaReq.bucket, user=self.utakaReq.user)
				#SET HEADERS
			elif self.utakaReq.req.method == 'POST':
				'''POST'''
			elif self.utakaReq.req.method == 'COPY':
				'''COPY'''


	def __copyOperation(self):
		pass


	def __postOperation(self):
		pass


	def __deleteOperation(self):
		result = destroyBucket(bucket=self.utakaReq.bucket, user=self.utakaReq.user)


	def __putOperation(self):
		result = setBucket(bucket = self.utakaReq.bucket, user = self.utakaReq.user)


	def __getOperation(self):
		getBucketParams = {'name':self.utakaReq.bucket}
		for param in 'prefix', 'marker', 'max-keys', 'delimiter':
			if param in self.utakaReq.subresources:
				getBucketParams[param] = self.utakaReq.subresources[param]
		res = getBucket(bucket = self.utakaReq.bucket, user = self.utakaReq.user,
					prefix = getBucketParams.get('prefix'), marker = getBucketParams.get('marker'),
					maxKeys = getBucketParams.get('max-keys'), delimiter = getBucketParams.get('delimiter'))


	def __putLoggingOperation(self):
		pass


	def __getLoggingOperation(self):
		pass


	def __putAclOperation(self):
		pass


	def __getAclOperation(self):
		pass


	def __getBucketXMLResponse(self, bucketDictionary, contentDictionaryList, commonPrefixesList):
		import xml.dom.minidom
		doc = xml.dom.minidom.Document()

		nameEl = doc.createElement("Name")
		nameEl.appendChild(bucketDictionary.get('name'))

		prefixEl = doc.createElement("Prefix")
		prefixEl.appendChild(doc.createTextNode(bucketDictionary.get('prefix', '')))

		markerEl = doc.createElement("Marker")
		markerEl.appendChild(doc.createTextNode(bucketDictionary.get('marker', '')))

		maxkeysEl = doc.createElement("MaxKeys")
		maxkeysEl.appendChild(doc.createTextNode(bucketDictionary.get('maxKeys', '')))

		truncatedEl= doc.createElement("IsTruncated")
		truncatedEl.appendChild(doc.createTextNode(bucketDictionary.get('isTruncated', '')))

		contentsEl = doc.createElement("Contents")
		for val in contentDictionaryList:
			keyEl = doc.createElement("Key")
			keyEl.appendChild(doc.createTextNode(val['key']))

			lastModifiedEl = doc.createElement("LastModified")
			lastModifiedEl.appendChild(doc.createTextNode(val['lastModified']))

			eTagEl = doc.createElement("ETag")
			eTagEl.appendChild(doc.createTextNode(val['eTag']))

			sizeEl = doc.createElement("Size")
			sizeEl.appendChild(doc.createTextNode(val['size']))

			storageClassEl = doc.createElement("StorageClass")
			storageClassEl.appendChild(doc.createTextNode("STANDARD"))

			ownerEl = doc.createElement("Owner")
			ownerIdEl = doc.createElement("ID")
			ownerIdEl.appendChild(doc.createTextNode(val['owner']['id']))
			ownerNameEl = doc.createElement("DisplayName")
			ownerNameEl.appendChild(doc.createTextNode(val['owner']['name']))
			ownerEl.appendChild(ownerIdEl)
			ownerEl.appendChild(ownerNameEl)

			contentsEl.appendChild(keyEl)
			contentsEl.appendChild(lastModifiedEl)
			contentsEl.appendChild(eTagEl)
			contentsEl.appendChild(sizeEl)
			contentsEl.appendChild(storageClassEl)
			contentsEl.appendChild(ownerEl)

		if commonPrefixesList:
			commonPrefixesEl = doc.createElement("CommonPrefixes")
			for val in commonPrefixesList:
				prefixEl = doc.createElement("Prefix")
				prefixEl.appendChild(doc.createTextNode(val))
				commonPrefixesEl.appendChild(prefixEl)

		listBucketEl = doc.createElement("ListBucketResult")
		listBucketEl.appendChild(nameEl)
		listBucketEl.appendChild(prefixEl)
		listBucketEl.appendChild(markerEl)
		listBucketEl.appendChild(maxkeysEl)
		listBucketEl.appendChild(truncatedEl)
		listBucketEl.appendChild(contentsEl)
		if commonPrefixesEl:
			listBucketEl.appendChild(commonPrefixesEl)

		doc.appendChild(listBucketEl)
		return doc.toxml('utf-8')