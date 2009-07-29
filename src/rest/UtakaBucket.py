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
import xml.dom.minidom
import utaka.src.core.BucketWithACPAndLog as Bucket
import utaka.src.accessControl.BucketACP as BucketACP

class UtakaBucket:

	def __init__(self, utakaReq):
		self.utakaReq = utakaReq


	def handleRequest(self):

		if 'acl' in self.utakaReq.subresources:
			if self.utakaReq.req.method == 'GET':
				operation = self.__getAclOperation
			elif self.utakaReq.req.method == 'PUT':
				operation = self.__putAclOperation
		elif 'logging' in self.utakaReq.subresources:
			if self.utakaReq.req.method == 'GET':
				operation = self.__getLoggingOperation
			elif self.utakaReq.req.method == 'PUT':
				operation = self.__putLoggingOperation
		elif self.utakaReq.req.method == 'GET':
			operation = self.__getOperation
		elif self.utakaReq.req.method == 'PUT':
			operation = self.__putOperation
		elif self.utakaReq.req.method == 'DELETE':
			operation = self.__deleteOperation
		elif self.utakaReq.req.method == 'POST':
			operation = self.__postOperation
		elif self.utakaReq.req.method == 'COPY':
			operation = self.__copyOperation

		return operation()


	def __copyOperation(self):
		pass


	def __postOperation(self):
		pass


	def __deleteOperation(self):
		result = Bucket.destroyBucket(bucket=self.utakaReq.bucket, user=self.utakaReq.user)


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
		result = Bucket.setBucket(bucket = self.utakaReq.bucket, user = self.utakaReq.user, accessControlPolicy = acp)


	def __getOperation(self):
		getBucketParams = {'name':self.utakaReq.bucket}
		for param in 'prefix', 'marker', 'max-keys', 'delimiter':
			if param in self.utakaReq.subresources:
				getBucketParams[param] = self.utakaReq.subresources[param]
		res = Bucket.getBucket(bucket = self.utakaReq.bucket, user = self.utakaReq.user,
					prefix = getBucketParams.get('prefix'), marker = getBucketParams.get('marker'),
					maxKeys = getBucketParams.get('max-keys'), delimiter = getBucketParams.get('delimiter'))
		getBucketParams['isTruncated'] = str(res[2])
		self.utakaReq.req.content_type = 'application/xml'
		self.utakaReq.write(self.__getXMLResponse(getBucketParams, res[0], res[1]))

	def __putLoggingOperation(self):
		pass


	def __getLoggingOperation(self):
		Bucket.getBucketLogStatus(user=self.utakaReq.user, bucket=self.utakaReq.bucket)



	def __putAclOperation(self):
		#READ BODY
		acl = self.__getAclFromXMLRequest()
		Bucket.putBucketACP(user=self.utakaReq.user, bucket=self.utakaReq.bucket, accessControlList=acl)
		pass


	def __getAclOperation(self):
		bucket_acp = Bucket.getBucketACP(bucket=self.utakaReq.bucket, user=self.utakaReq.user)
		if len(bucket_acp) == 0:
			'''bucket not found, throw error'''
		else:
			self.utakaReq.write(self.__getAclXMLResponse(bucket_acp))

	def __getAclFromXMLRequest(self):
		dom = xml.dom.minidom.parseString(self.utakaReq.req.read())



	def __getAclXMLResponse(self, bucket_acp):
		doc = xml.dom.minidom.Document()

		oidEl = doc.createElement("ID")
		oidEl.appendChild(doc.createTextNode(str(bucket_acp[0]['userid'])))

		onameEl = doc.createElement("DisplayName")
		onameEl.appendChild(doc.createTextNode(bucket_acp[0]['username']))

		ownerEl = doc.createElement("Owner")
		ownerEl.appendChild(oidEl)
		ownerEl.appendChild(onameEl)

		aclEl = doc.createElement("AccessControlList")
		for row in bucket_acp[1:]:

			gidEl = doc.createElement("ID")
			gidEl.appendChild(doc.createTextNode(str(row['userid'])))

			gnameEl= doc.createElement("DisplayName")
			gnameEl.appendChild(doc.createTextNode(row['username']))

			granteeEl = doc.createElement("Grantee")
			granteeEl.setAttribute("type", "CanonicalUser")
			granteeEl.appendChild(gidEl)
			granteeEl.appendChild(gnameEl)

			permissionEl = doc.createElement("Permission")
			permissionEl.appendChild(doc.createTextNode(row['permission'].upper()))

			grantEl = doc.createElement("Grant")
			grantEl.appendChild(granteeEl)
			grantEl.appendChild(permissionEl)

			aclEl.appendChild(grantEl)

		acpEl = doc.createElement("AccessControlPolicy")
		acpEl.appendChild(ownerEl)
		acpEl.appendChild(aclEl)
		doc.appendChild(acpEl)
		return doc.toxml('utf-8')


	def __getXMLResponse(self, bucketDictionary, contentDictionaryList, commonPrefixesList):
		doc = xml.dom.minidom.Document()

		nameEl = doc.createElement("Name")
		nameEl.appendChild(doc.createTextNode(bucketDictionary['name']))

		prefixEl = doc.createElement("Prefix")
		if 'prefix' in bucketDictionary:
			prefixEl.appendChild(doc.createTextNode(bucketDictionary['prefix']))

		markerEl = doc.createElement("Marker")
		if 'marker' in bucketDictionary:
			markerEl.appendChild(doc.createTextNode(bucketDictionary['marker']))

		maxkeysEl = doc.createElement("MaxKeys")
		if 'maxKeys' in bucketDictionary:
			maxkeysEl.appendChild(doc.createTextNode(bucketDictionary['maxKeys']))

		truncatedEl= doc.createElement("IsTruncated")
		truncatedEl.appendChild(doc.createTextNode(bucketDictionary['isTruncated']))

		contentsEl = doc.createElement("Contents")
		commonPrefixesEl = None
		for val in contentDictionaryList:
			keyEl = doc.createElement("Key")
			keyEl.appendChild(doc.createTextNode(val['key']))

			lastModifiedEl = doc.createElement("LastModified")
			lastModifiedEl.appendChild(doc.createTextNode(val['lastModified']))

			eTagEl = doc.createElement("ETag")
			eTagEl.appendChild(doc.createTextNode(val['eTag']))

			sizeEl = doc.createElement("Size")
			sizeEl.appendChild(doc.createTextNode(str(val['size'])))

			storageClassEl = doc.createElement("StorageClass")
			storageClassEl.appendChild(doc.createTextNode("STANDARD"))

			ownerEl = doc.createElement("Owner")
			ownerIdEl = doc.createElement("ID")
			ownerIdEl.appendChild(doc.createTextNode(str(val['owner']['id'])))
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