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
Created July, 2009

methods for converting accessControlPolicy between a dictionary and xml string representation
@author: Andrew
'''
import xml.dom.minidom
import utaka.src.exceptions.BadRequestException as BadRequestException

def toXML(accessControlPolicy):
	'''converts an acp dictionary into an xml string'''
	doc = xml.dom.minidom.Document()
	#AccessControlPolicy
	acpEl = doc.createElement("AccessControlPolicy")
	acpEl.setAttribute('xmlns', "http://s3.amazonaws.com/doc/2006-03-01/")
	#-Owner
	ownerEl = doc.createElement("Owner")
	#--ID
	oidEl = doc.createElement("ID")
	oidEl.appendChild(doc.createTextNode(str(accessControlPolicy['owner']['userid'])))
	ownerEl.appendChild(oidEl)
	#--DisplayName
	onameEl = doc.createElement("DisplayName")
	onameEl.appendChild(doc.createTextNode(accessControlPolicy['owner']['username']))
	ownerEl.appendChild(onameEl)
	acpEl.appendChild(ownerEl)
	#-AccessControlList
	aclEl = doc.createElement("AccessControlList")
	for row in accessControlPolicy['acl']:
		#Grant
		grantEl = doc.createElement("Grant")
		#-Grantee
		granteeEl = doc.createElement("Grantee")
		granteeEl.setAttribute("type", "CanonicalUser")
		#--ID
		gidEl = doc.createElement("ID")
		gidEl.appendChild(doc.createTextNode(str(row['grantee']['userid'])))
		granteeEl.appendChild(gidEl)
		#--DisplayName
		gnameEl = doc.createElement("DisplayName")
		gnameEl.appendChild(doc.createTextNode(row['grantee']['username']))
		granteeEl.appendChild(gnameEl)
		grantEl.appendChild(granteeEl)
		#-Permission
		permEl = doc.createElement("Permission")
		permEl.appendChild(doc.createTextNode(row['permission'].upper()))
		grantEl.appendChild(permEl)
		aclEl.appendChild(grantEl)
	acpEl.appendChild(aclEl)
	doc.appendChild(acpEl)
	return doc.toxml('utf-8')


def fromXML(xmlString):
	'''converts an xml string to an acp dictionary'''
	try:
		dom = xml.dom.minidom.parseString(xmlString)
	except:
		raise BadRequestException.MalformedACLErrorException()
	if len(dom.childNodes) != 1 or dom.childNodes[0].nodeName != 'AccessControlPolicy':
		raise BadRequestException.MalformedACLErrorException()
	acpEl = dom.childNodes[0]
	result = {}
	if len(acpEl.childNodes) != 2:
		raise BadRequestException.MalformedACLErrorException()
	if acpEl.childNodes[0].nodeName == 'Owner' and acpEl.childNodes[1].nodeName == 'AccessControlList':
		result['owner'] = __buildUserFromXML(acpEl.childNodes[0])
		result['acl'] = __buildACLFromXML(acpEl.childNodes[1])
	elif acpEl.childNodes[0].nodeName == 'AccessControlList' and acpEl.childNodes[1].nodeName == 'Owner':
		result['owner'] = __buildUser(acpEl.childNodes[1])
		result['acl'] = __buildACLFromXML(acpEl.childNodes[0])
	else:
		raise BadRequestException.MalformedACLErrorException()
	return result


def __buildACLFromXML(aclXmlNode):
	'''fromXML helper method, given proper xml acl node, returns acl dictionary list'''
	acl = []
	for node in aclXmlNode.childNodes:
		if node.nodeName != 'Grant':
			raise BadRequestException.MalformedACLErrorException()
		if len(node.childNodes) != 2:
			raise BadRequestException.MalformedACLErrorException()
		if node.childNodes[0].nodeName == 'Grantee' and node.childNodes[1].nodeName == 'Permission':
			acl.append({'grantee': __buildUserFromXML(node.childNodes[0]), 'permission' : __buildPermissionFromXML(node.childNodes[1])})
		elif node.childNodes[1].nodeName == 'Grantee' and node.childNodes[0].nodeName == 'Permission':
			acl.append({'grantee': __buildUserFromXML(node.childNodes[1]), 'permission' : __buildPermissionFromXML(node.childNodes[0])})
		else:
			raise BadRequestException.MalformedACLErrorException()
	return acl


def __buildUserFromXML(userNode):
	'''fromXML helper method, given proper xml user node, returns user dictionary'''
	user = {}
	if len(userNode.childNodes) == 1:
		if userNode.childNodes[0].nodeName != 'ID':
			raise BadRequestException.MalformedACLErrorException()
		user['userid'] = __getNodeText(userNode.childNodes[0].childNodes)
	elif len(userNode.childNodes) == 2:
		if userNode.childNodes[0].nodeName == 'ID' and userNode.childNodes[1].nodeName == 'DisplayName':
			user['userid'] = __getNodeText(userNode.childNodes[0].childNodes)
			user['username'] = __getNodeText(userNode.childNodes[1].childNodes)
		elif userNode.childNodes[1].nodeName == 'ID' and userNode.childNodes[0].nodeName == 'DisplayName':
			user['userid'] = __getNodeText(userNode.childNodes[1].childNodes)
			user['username'] = __getNodeText(userNode.childNodes[0].childNodes)
		else:
			raise BadRequestException.MalformedACLErrorException()
	else:
		raise BadRequestException.MalformedACLErrorException()
	return user


def __buildPermissionFromXML(permissionNode):
	'''fromXML helper method, given proper permission node, validates and returns text'''
	permission = __getNodeText(permissionNode.childNodes)
	if permission not in ('READ', 'WRITE', 'READ_ACP', 'WRITE_ACP', 'FULL_CONTROL'):
		raise BadRequestException.MalformedACLErrorException()
	return permission


def __getNodeText(nodelist):
	'''fromXML helper method, returns string concatination of all the node list's text nodes'''
	rc = ""
	for node in nodelist:
		if node.nodeType == node.TEXT_NODE:
			rc = rc+ node.data
	return rc
