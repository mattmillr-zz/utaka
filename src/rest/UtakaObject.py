'''
Created on Jul 21, 2009

@author: Andrew
'''

import utaka.src.core.ObjectWithACP as Object
import utaka.src.accessControl.ObjectACP as ObjectACP
import utaka.src.accessControl.AcpXml as AcpXml


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
		object_acp = Object.getObjectACP(self.utakaReq.user, self.utakaReq.bucket, self.utakaReq.key)
		if len(object_acp) == 0:
			'''object not found, throw error'''
		else:
			self.utakaReq.req.content_type = 'application/xml'
			self.utakaReq.write(AcpXml.toXML(object_acp))


	def __putAclOperation(self):
		acp = AcpXml.fromXML(self.utakaReq.req.read())
		Object.setObjectACP(self.utakaReq.user, self.utakaReq.bucket, self.utakaReq.key, acp)


	def __postOperation(self):
		'''implement later'''


	def __copyOperation(self):
		#get source key and bucket
		sourceURI = self.utakaReq.customHeadersTable.get('copy-source')
		if sourceURI:
			import urllib
			srcUriDigestResult = self.utakaReq.uriDigest(urllib.unquote(sourceURI))
			skey = srcUriDigestResult['key']
			sbucket = srcUriDigestResult['bucket']
		else:
			'''incorrect args, raise error'''
		#get metadata directive
		metadataDirective = self.utakaReq.customHeadersTable('metadata-directive', 'COPY')
		metadata = None
		if metadataDirective == 'REPLACE':
			metadata = __getMetadata()
		elif metadataDirective == 'COPY':
			if skey == self.utakaReq.key:
				'''cannot copy same object unless directive set to replace, raise error'''
		else:
			'''directive must be copy or replace, raise error'''
		result = cloneObject(self.utakaReq.user, sbucket, skey, self,utakaReq.bucket, self.utakaReq.key, metadata, self.utakaReq.customHeadersTable.get('if-match'), self.utakaReq.customHeadersTable.get('if-none-match'), self.utakaReq.customHeadersTable.get('if-modified-since'), self.utakaReq.customHeadersTable.get('if-unmodified-since'))


	def __getOperation(self, getData=True):
		startRange, endRange = self.__digestRange()
		result = Object.getObject( user = self.utakaReq.user,
			bucket=self.utakaReq.bucket, key=self.utakaReq.key,
			byteRangeStart = startRange, byteRangeEnd = endRange,
			ifModifiedSince=self.utakaReq.req.headers_in.get('if-modified-since'),
			ifNotModifiedSince=self.utakaReq.req.headers_in.get('if-unmodified-since'),
			ifMatch = self.utakaReq.req.headers_in.get('if-match'),
			ifNotMatch = self.utakaReq.req.headers_in.get('if-none-match'),
			ifRange = self.utakaReq.req.headers_in.get('if-range'),
			getMetadata = True, getData = getData)
		self.utakaReq.req.headers_out['ETag'] = result['eTag']
		self.utakaReq.req.headers_out['Content-Length'] = str(result['size'])
		self.utakaReq.req.content_type = result['content-type']
		self.utakaReq.req.headers_out['Last-Modified'] = result['lastModified']
		if 'content-encoding' in result:
			self.utakaReq.req.headers_out['Content-Encoding'] = result['content-encoding']
		if 'content-disposition' in result:
			self.utakaReq.req.headers_out['Content-Disposition'] = result['content-disposition']
		if 'content-range' in result:
			self.utakaReq.req.headers_out['Content-Range'] = result['content-range']
		if 'metadata' in result:
			for tag, val in result['metadata']:
				self.utakaReq.req.headers_out[self.utakaReq.customHeaderPrefix + tag] = val
		if getData:
			self.utakaReq.write(result['data'])
			#result - eTag, contentLength, contentType, contentRange, lastModified, metadata, data


	def __putOperation(self):
		cannedACL = self.utakaReq.customHeaderTable.get('acl', 'private')
		acp = {}
		acp['owner'] = {'userid':self.utakaReq.user}
		acl = [{'grantee':{'userid':self.utakaReq.user}, 'permission':'FULL_CONTROL'}]
		if cannedACL == 'public-read':
			acl.append({'grantee':{'userid':1}, 'permission':'read'})
		elif cannedACL == 'public-read-write':
			acl.append({'grantee':{'userid':1}, 'permission':'read'})
			acl.append({'grantee':{'userid':1}, 'permission':'write'})
		elif cannedACL == 'authenticated-read':
			acl.append({'grantee':{'userid':2}, 'permission':'read'})
		elif cannedACL != 'private':
			'''throw error'''
		acp['acl'] = acl
				
		result = Object.setObject( user = self.utakaReq.user,
			bucket = self.utakaReq.bucket, key=self.utakaReq.key,
			contentDisposition = self.utakaReq.req.headers_in.get('content-disposition'),
			contentEncoding = self.utakaReq.req.headers_in.get('content-encoding'),
			contentType = self.utakaReq.req.headers_in.get('content-type'),
			contentMd5 = self.utakaReq.req.headers_in.get('content-md5'),
			metadata = self.__getMetadata(),
			accessControlPolicy = acp,
			data = self.utakaReq.req.read())


	def __headOperation(self):
		return __getOperation(False)


	def __deleteOperation(self):
		result = Object.destroyObject(key = self.utakaReq.key, bucket = self.utakaReq.bucket, user = self.utakaReq.user)


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

	def __getMetadata(self):
		#get metadata
		metadata = {}
		for val in self.utakaReq.customHeaderTable.keys():
			if val.lower().startswith('meta-'):
				metadata[val.lower()[len('meta-'):]] = self.utakaReq.customHeaders[val]
		return metadata