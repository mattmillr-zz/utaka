'''
Created on Jul 21, 2009

UtakaService currently only implements GET which returns a list of buckets of that user
	later methods may be added for admin purposes
@author: Andrew
'''


from mod_python import apache

class UtakaService:

	'''INIT'''
	def __init__(self, utakaReq):
		self.req = utakaReq



	'''HANDLE REQUEST'''
	def handleRequest(self):
		if self.req.method == 'GET':
			operation = __getOperation()
		else:
			raise apache.SERVER_RETURN, apache.HTTP_NOT_IMPLEMENTED

		return operation()

	'''GET'''
	def __getOperation(self):
		try:
			result = Utaka.src.core.service.getService(self.req.user)
		except Exception, e:
			pass
		else:
			userDict = result['user']
			listOfBuckets = result['buckets']
			self.req.req.content_type = 'application/xml'
			self.req.write(self.__getServiceXMLResponse(userDict, listOfBuckets))

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
		ownerIdEl.appendChild(doc.createTextNode(userDictionary['userid']))
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