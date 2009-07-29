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
import utaka.src.errors.DataAccessErrors

'''
UtakaService currently only implements GET which returns a list of buckets of that user
	later methods may be added for admin purposes
'''
class UtakaService:


	def __init__(self, utakaReq):
		self.utakaReq = utakaReq


	def handleRequest(self):
		if self.utakaReq.req.method == 'GET':
			operation = self.__getOperation
		else:
			raise Exception

		return operation()


	def __getOperation(self):
		import utaka.src.core.Service as Service
		result = Service.getService(self.utakaReq.user)
		userDict = result['user']
		listOfBuckets = result['buckets']
		self.utakaReq.req.content_type = 'application/xml'
		self.utakaReq.write(self.__getServiceXMLResponse(userDict, listOfBuckets))
		return apache.OK


	def __getServiceXMLResponse(self, userDictionary, bucketDictionaryList):
		import xml.dom.minidom
		doc = xml.dom.minidom.Document()
		listAllBucketsEl = doc.createElement("ListAllMyBucketsResult")
		ownerEl = doc.createElement("Owner")
		ownerIdEl = doc.createElement("ID")
		ownerNameEl = doc.createElement("DisplayName")
		bucketListEl = doc.createElement("Buckets")
		doc.appendChild(listAllBucketsEl)

		#owner
		listAllBucketsEl.appendChild(ownerEl)
		ownerEl.appendChild(ownerIdEl)
		ownerIdEl.appendChild(doc.createTextNode(str(userDictionary['userId'])))
		ownerEl.appendChild(ownerNameEl)
		ownerNameEl.appendChild(doc.createTextNode(userDictionary['username']))

		#bucket list
		listAllBucketsEl.appendChild(bucketListEl)
		for val in bucketDictionaryList:
			bucketEl= doc.createElement("Bucket")
			bucketNameEl = doc.createElement("Name")
			bucketDateEl = doc.createElement("CreationDate")
			bucketListEl.appendChild(bucketEl)
			bucketEl.appendChild(bucketNameEl)
			bucketNameEl.appendChild(doc.createTextNode(val['bucketName']))
			bucketEl.appendChild(bucketDateEl)
			bucketDateEl.appendChild(doc.createTextNode(val['creationDate']))

		return doc.toxml('utf-8')