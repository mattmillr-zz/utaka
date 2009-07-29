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
				#raise error
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
		pass


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
			#raise error
		metadataDirective = self.utakaReq.customHeadersTable('metadata-directive', 'COPY')
		metadata = None
		if metadataDirective == 'REPLACE':
			#GET METADATA
			for val in self.utakaReq.customHeaders.keys():
				if val.lower().startswith('meta-'):
					metadata[val.lower()[len('meta-'):]] = self.utakaReq.customHeaders[val]
		elif metadataDirective == 'COPY':
			if skey == self.utakaReq.key:
				#raise error
		else:
			#raise error
		result = cloneObject( user = self.utakaReq.user, sourceKey = skey,
			sourceBucket = sbucket, destinationKey = self.utakaReq.key,
			destinationBucket = self.utaka.bucket, metadata = metadata,
			ifModifiedSince=self.utakaReq.customHeadersTable.get('if-modified-since'),
			ifUnmodifiedSince=self.utakaReq.customHeadersTable.get('if-unmodified-since'),
			ifMatch = self.utakaReq.customHeadersTable.get('if-match'),
			ifNoneMatch = self.utakaReq.customHeadersTable.get('if-none-match'))


	def __getOperation(self):
		startRange, endRange = __digestRange()
		result = getObject( user = self.utakaReq.user,
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
			contentLength = self.utakaReq.req.headers_in.get('content-length')
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
		return int(startRange), int(endRange)
