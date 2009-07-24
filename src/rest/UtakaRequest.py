'''
Created on Jul 21, 2009
UtakaRequest
wraps an apache request
adds:
	user
	key
	bucket
	subresources - dict of query string keys and vals
	customHeaderPrefix -
	customHeaderTable - dict of headers that began with the customHeaderPrefix, prefix has been stripped
@author: Andrew
'''

from mod_python import apache
from utaka.src.rest.HMAC_SHA1_Authentication import getUser
import utaka.src.config as config

class UtakaRequest:

	def __init__(self, req, virtualBucket=False):

		self.req = req
		self.bucket = self.key = None
		self.subresources = {}

		#Query string digest
		if self.req.args:
			self.subresources = util.parse_qs(self.req.args, True)
			if 'logging' in self.subresources:
				if 'acl' in self.subresources or 'torrent' in self.subresources or 'location' in self.subresources:
					'''raise error'''
			elif 'acl' in self.subresources:
				if 'torrent' in self.subresources or 'location' in subresources:
					'''raise error'''
			elif 'torrent' in self.subresources:
				if 'location' in subresources:
					'''raise error'''

		#URI digest
		uriDigestResults = uriDigest(req.uri)
		self.bucket = uriDigestResults.get('bucket')
		self.key = uriDigestResults.get('key')

		#custom header table
		try:
			self.customHeaderPrefix = config.get('common', 'customHeaderPrefix').lower()
		except Exception:
			raise apache.SERVER_RETURN, apache.HTTP_INTERNAL_SERVER_ERROR

		self.customHeaderTable = {}
		for val in self.req.headers_in.keys():
			if val.lower().startswith(self.customHeaderPrefix):
				self.customHeaderTable[val.lower()[len(self.customHeaderPrefix):]] = self.req.headers_in[val]

		#Get Authenticated User
		self.user = getUser(req)

		#Check date
		#check customDateHeader then date header

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