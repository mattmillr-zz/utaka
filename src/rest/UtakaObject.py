'''
Created on Jul 21, 2009

@author: Andrew
'''

import utaka.src.core.Object as Object
import utaka.src.accessControl.ObjectACP as ObjectACP
import xml.dom.minidom


class UtakaObject:

	def __init__(self, utakaReq):
		self.utakaReq = utakaReq


	def handleRequest(self):
		if 'acl' in self.utakaReq.subresources:
			if self.utakaReq.req.method == 'GET':
				operation = self.__getAclOperation
			elif self.utakaReq.req.method == 'PUT':
				operation = self.__putAclOperation
			else:
				'''raise error'''
		elif self.utakaReq.req.method == 'GET':
			operation = self.__getOperation
		elif self.utakaReq.req.method == 'PUT':
			operation = self.__putOperation
		elif self.utakaReq.req.method == 'POST':
			operation = self.__postOperation
		elif self.utakaReq.req.method == 'HEAD':
			operation = self.__headOperation
		elif self.utakaReq.req.method == 'COPY':
			operation = self.__copyOperation
		elif self.utakaReq.req.method == 'DELETE':
			operation = self.__deleteOperation

		return operation()


	def __getAclOperation(self):
		object_acp = ObjectACP.getObjectACP(key = self.utakaReq.key, bucket = self.utakaReq.bucket)
		if len(object_acp) == 0:
			'''object not found, throw error'''
		else:
			self.utakaReq.write(self.__getAclXMLResponse(object_acp))


	def __putAclOperation(self):
		pass


	def __postOperation(self):
		pass


	def __copyOperation(self):
		sourceURI = self.utakaReq.customHeadersTable.get('copy-source')
		if sourceURI:
			import urllib
			srcUriDigestResult = self.utakaReq.uriDigest(urllib.unquote(sourceURI))
			skey = srcUriDigestResult['key']
			sbucket = srcUriDigestResult['bucket']
		else:
			'''incorrect args, raise error'''
		metadataDirective = self.utakaReq.customHeadersTable('metadata-directive', 'COPY')
		metadata = None
		if metadataDirective == 'REPLACE':
			#GET METADATA
			for val in self.utakaReq.customHeaders.keys():
				if val.lower().startswith('meta-'):
					metadata[val.lower()[len('meta-'):]] = self.utakaReq.customHeaders[val]
		elif metadataDirective == 'COPY':
			if skey == self.utakaReq.key:
				'''cannot copy same object unless directive set to replace, raise error'''
		else:
			'''directive must be copy or replace, raise error'''
		result = cloneObject( user = self.utakaReq.user, sourceKey = skey,
			sourceBucket = sbucket, destinationKey = self.utakaReq.key,
			destinationBucket = self.utaka.bucket, metadata = metadata,
			ifModifiedSince=self.utakaReq.customHeadersTable.get('if-modified-since'),
			ifUnmodifiedSince=self.utakaReq.customHeadersTable.get('if-unmodified-since'),
			ifMatch = self.utakaReq.customHeadersTable.get('if-match'),
			ifNoneMatch = self.utakaReq.customHeadersTable.get('if-none-match'))


	def __getOperation(self):
		startRange, endRange = self.__digestRange()
		result = Object.getObject( userId = self.utakaReq.user,
			bucket=self.utakaReq.bucket, key=self.utakaReq.key,
			byteRangeStart = startRange, byteRangeEnd = endRange,
			ifModifiedSince=self.utakaReq.req.headers_in.get('if-modified-since'),
			ifUnmodifiedSince=self.utakaReq.req.headers_in.get('if-unmodified-since'),
			ifMatch = self.utakaReq.req.headers_in.get('if-match'),
			ifNoneMatch = self.utakaReq.req.headers_in.get('if-none-match'),
			ifRange = self.utakaReq.req.headers_in.get('if-range'),
			getMetaData = True, getData = True)
			#result - eTag, contentLength, contentType, contentRange, lastModified, metadata, data


	def __putOperation(self):
		result = setObject( user = self.utakaReq.user,
			bucket = self.utakaReq.bucket, key=self.utakaReq.key,
			contentDisposition = self.utakaReq.req.headers_in.get('content-disposition'),
			contentEncoding = self.utakaReq.req.headers_in.get('content-encoding'),
			contentType = self.utakaReq.req.headers_in.get('content-type'),
			contentLength = self.utakaReq.req.headers_in.get('content-length'),
			metadata = self.utakaReq.customMetadata,
			acl = self.utakaReq.customAcl,
			data = self.utakaReq.req.read())


	def __headOperation(self):
		startRange, endRange = __digestRange()
		result = getObject( user = self.utakaReq.user,
			bucket=self.utakaReq.bucket, key=self.utakaReq.key,
			byteRangeStart = startRange, byteRangeEnd = endRange,
			ifModifiedSince=self.utakaReq.req.headers_in.get('if-modified-since'),
			ifUnmodifiedSince=self.utakaReq.req.headers_in.get('if-unmodified-since'),
			ifMatch = self.utakaReq.req.headers_in.get('if-match'),
			ifNoneMatch = self.utakaReq.req.headers_in.get('if-none-match'),
			ifRange = self.utakaReq.req.headers_in.get('if-range'),
			getMetaData = True, getData = False)


	def __deleteOperation(self):
		result = destroyObject(key = self.utakaReq.key, bucket = self.utakaReq.bucket, user = self.utakaReq.user)


	def __digestRange(self):
		startRange = endRange = None
		if self.utakaReq.req.range:
			range = (self.utaka.Req.req.range).trim()
			splitRange = range.split('bytes=')
			if len(splitRange) < 2:
				startRange, endRange = splitRange[len(splitRange)-1].split('-')
				startRange = int(startRange)
				endRange = int(endRange)
			else:
				'''raise exception'''
		return startRange, endRange
		
	def __getAclXMLResponse(self, object_acp):
		doc = xml.dom.minidom.Document()
		
		oidEl = doc.createElement("ID")
		oidEl.appendChild(doc.createTextNode(str(object_acp[0]['userid'])))
		
		onameEl = doc.createElement("DisplayName")
		onameEl.appendChild(doc.createTextNode(object_acp[0]['username']))
		
		ownerEl = doc.createElement("Owner")
		ownerEl.appendChild(oidEl)
		ownerEl.appendChild(onameEl)
		
		aclEl = doc.createElement("AccessControlList")
		for row in object_acp[1:]:
		
			gidEl = doc.createElement("ID")
			gidEl.appendChild(doc.createTextNode(str(row['userid'])))
			
			gnameEl= doc.createElement("DisplayName")
			gnameEl.appendChild(doc.createTextNode(row['username']))
			
			granteeEl = doc.createElement("Grantee")
			granteeEl.setAttribute("type", "CanonicalUser")
			granteeEl.appendChild(gidEl)
			granteeEl.appendChild(gnameEl)
			
			permissionEl = doc.createElement("Permission")
			permissionEl.appendChild(doc.createElement(row['permission'].upper()))
			
			grantEl = doc.createElement("Grant")
			grantEl.appendChild(granteeEl)
			grantEl.appendChild(permissionEl)
			
			aclEl.appendChild(grantEl)
			
		acpEl = doc.createElement("AccessControlPolicy")
		acpEl.appendChild(ownerEl)
		acpEl.appendChild(aclEl)
		doc.appendChild(acpEl)
		return doc.toxml('utf-8')
