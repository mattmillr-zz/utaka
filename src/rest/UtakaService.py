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
Created on Jul 10, 2009

@author: Andrew
'''

from mod_python import apache
import utaka.src.exceptions.MethodNotAllowedException as MethodNotAllowedException
import utaka.src.exceptions.ForbiddenException as ForbiddenException
import utaka.src.core.Service as Service


class UtakaService:
	'''implements service functionalities; get for normal users and put/delete for admin'''

	def __init__(self, utakaReq):
		self.utakaReq = utakaReq

	def handleRequest(self):
		if self.utakaReq.req.method == 'GET':
			operation = self.__getOperation
		elif not self.utakaReq.isUserAdmin:
			raise MethodNotAllowedException.ServiceMethodNotAllowedException(self.utakaReq.req.method)
		elif self.utakaReq.req.method == 'PUT':
			operation = self.__putOperation
		elif self.utakaReq.req.method == 'DELETE':
			operation = self.__deleteOperation
		else:
			raise MethodNotAllowedException.ServiceMethodNotAllowedException(self.utakaReq.req.method)
		return operation()

	def __putOperation(self):
		if 'newadmin' in self.utakaReq.customHeaderTable:
			results = Service.setService(self.utakaReq.customHeaderTable['newadmin'])
		else:
			results = Service.setService(self.utakaReq.customHeaderTable['newuser'])
		self.utakaReq.write('accesskey:%s\r\n' % results[0])
		self.utakaReq.write('secretkey:%s\r\n' % results[1])

	def __deleteOperation(self):
		pass

	def __getOperation(self):
		if self.utakaReq.user:
			result = Service.getService(self.utakaReq.user)
			userDict = result['user']
			listOfBuckets = result['buckets']
			self.utakaReq.req.content_type = 'application/xml'
			self.utakaReq.write(self.__getServiceXMLResponse(userDict, listOfBuckets))
		else:
			raise ForbiddenException.AccessDeniedException()

	def __getServiceXMLResponse(self, userDictionary, bucketDictionaryList):
		'''converts bucket dictionary into xml string'''
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