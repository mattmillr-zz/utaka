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
from mod_python import util
from utaka.src.rest.HMAC_SHA1_Authentication import getUser
import utaka.src.config as config


'''
UtakaRequest
wraps an apache request
adds:
	user
	key
	bucket
	subresources - dict of query string keys and vals
	customHeaderPrefix -
	customHeaderTable - dict of headers that began with the customHeaderPrefix, prefix has been stripped
'''
class UtakaRequest:

	def __init__(self, req, virtualBucket=False):

		self.req = req
		self.bucket = self.key = self.user = self.accesskey = self.signature = self.stringToSign = None
		self.subresources = {}
		self.__writeBuffer = ''

		#Query string digest
		if self.req.args:
			self.subresources = util.parse_qs(self.req.args, True)
			if 'logging' in self.subresources:
				if 'acl' in self.subresources or 'torrent' in self.subresources or 'location' in self.subresources:
					'''raise error'''
			elif 'acl' in self.subresources:
				if 'torrent' in self.subresources or 'location' in self.subresources:
					'''raise error'''
			elif 'torrent' in self.subresources:
				if 'location' in self.subresources:
					'''raise error'''

		#URI digest
		basehost = config.get('server', 'hostname')
		if self.req.servername == basehost
			uriDigestResults = self.uriDigest(req.uri)
			self.bucket = uriDigestResults.get('bucket')
			self.key = uriDigestResults.get('key')
		else:
			splitHost = self.req.servername.split("." + basehost)
			if splitHost == 2:
				uriDigestResult = self.uriDigest(splitHost[0] + '/' + req.uri)
				self.bucket = riDigestResults.get('bucket')
				self.key = uriDigestResults.get('key')
			else:
				'''throw error'''

		#custom header table
		try:
			self.customHeaderPrefix = config.get('common', 'customHeaderPrefix').lower()
		except Exception:
			raise apache.SERVER_RETURN, apache.HTTP_INTERNAL_SERVER_ERROR
		else:
			self.customHeaderTable = {}
			for val in self.req.headers_in.keys():
				if val.lower().startswith(self.customHeaderPrefix):
					self.customHeaderTable[val.lower()[len(self.customHeaderPrefix):]] = self.req.headers_in[val]
				
		#authenticate -- must happen after custom header table is created
		self.accesskey, self.signature = self.__getAccessKeyAndSignature()
		if self.accesskey:
			self.stringToSign = self.__buildStringToSign()
			self.user, self.computedSig = getUser(self.signature, self.accesskey, self.stringToSign)

		#Check date
		#check customDateHeader then date header
		
		if 'signature' in self.subresources:
			self.write(self.computedSig + "\r\n")
			self.write(self.stringToSign + "\r\n")
			self.write(str(self.subresources) + "\r\n")
			self.send()
		
	def write(self, msg):
		self.__writeBuffer += msg

	def send(self):
		#self.req.content_type = 'application/xml'
		self.req.set_content_length(len(self.__writeBuffer))
		self.req.write(self.__writeBuffer)
		
	def uriDigest(self, uri):
		results = {}
		splitURI = uri.split('/', 2)
		for segment in splitURI[:]:
			if len(segment) == 0:
				splitURI.remove(segment)
		if len(splitURI) == 2:
			results['bucket'], results['key'] = splitURI[0], splitURI[1]
		elif len(splitURI) == 1:
			results['bucket'] = splitURI[0]
		return results
		
	def __buildStringToSign(self):
		nl = '\n'

		#http headers
		methodString = self.req.method
		contentMd5String = self.req.headers_in.get('content-md5', '')
		contentTypeString = self.req.headers_in.get('content-type', '')
		dateString = self.req.headers_in.get('date', '')

		#Canonicalize Custom Headers
		__customHeaderPrefix = config.get('common', 'customHeaderPrefix').lower()
		__customDateHeader = __customHeaderPrefix + "-date"

		customHeaderList = []
		canCustomHeaders = ''

		for tag, val in self.customHeaderTable.iteritems():
			#self.req.write(tag + ":" + value + "\r\n")
			customHeaderList.append(self.customHeaderPrefix + tag + ":" + val.lstrip() + nl)
			if val == 'date':
					dateString = ''
		customHeaderList.sort()
		for val in customHeaderList:
			canCustomHeaders += val

		#Canoicalize URI
		uriString = self.req.uri
		for val in ('acl',):
			#self.write("CHECKING FOR ACL\r\n")
			if val in self.subresources:
				#self.write("FOUND ACL\r\n")
				uriString += '?' + val
		return (methodString + nl + contentMd5String + nl +
			contentTypeString + nl + dateString + nl + canCustomHeaders + uriString)
		
		
	def __getAccessKeyAndSignature(self):
		try:
			header = config.get('authentication', 'header')
			prefix = config.get('authentication', 'prefix') + ' '
		except ServerException, e:
			raise exception, e
		else:
			try:
				authString = self.req.headers_in[header]
			except KeyError:
				return None, None
			else:
				splitAuth = authString.split(prefix)
				if len(splitAuth) == 2 and len(splitAuth[0]) == 0:
					try:
						accesskey, signature = splitAuth[1].split(':')
					except ValueError, e:
						raise exception, "BAD AUTH STRING"
					else:
						return accesskey, signature