
import xml.dom.minidom

def toXML(accessControlPolicy):

	doc = xml.dom.minidom.Document()

	#AccessControlPolicy
	acpEl = doc.createElement("AccessControlPolicy")

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
	dom = xml.dom.minidom.parseString(xmlString)
	if len(dom.childNodes) != 1 or dom.childNodes[0].nodeName != 'AccessControlPolicy':
		raise Exception, 'xml format'
	acpEl = dom.childNodes[0]

	result = {}
	if len(acpEl.childNodes) != 2:
		raise Exception, 'xml format'
	if acpEl.childNodes[0].nodeName == 'Owner' and acpEl.childNodes[1].nodeName == 'AccessControlList':
		result['owner'] = __buildUserFromXML(acpEl.childNodes[0])
		result['acl'] = __buildACLFromXML(acpEl.childNodes[1])
	elif acpEl.childNodes[0].nodeName == 'AccessControlList' and acpEl.childNodes[1].nodeName == 'Owner':
		result['owner'] = __buildUser(acpEl.childNodes[1])
		result['acl'] = __buildACLFromXML(acpEl.childNodes[0])
	else:
		raise Exception, 'xml format'
	return result

	
def __buildACLFromXML(aclXmlNode):
	acl = []
	for node in aclXmlNode.childNodes:
		if node.nodeName != 'Grant':
			raise Exception, 'xml format'
		if len(node.childNodes) != 2:
			raise Exception, 'xml format'
		if node.childNodes[0].nodeName == 'Grantee' and node.childNodes[1].nodeName == 'Permission':
			acl.append({'grantee': __buildUserFromXML(node.childNodes[0]), 'permission' : __buildPermissionFromXML(node.childNodes[1])})
		elif node.childNodes[1].nodeName == 'Grantee' and node.childNodes[0].nodeName == 'Permission':
			acl.append({'grantee': __buildUserFromXML(node.childNodes[1]), 'permission' : __buildPermissionFromXML(node.childNodes[0])})
		else:
			raise Exception, 'xml format'
	return acl

	
def __buildUserFromXML(userNode):
	user = {}
	if len(userNode.childNodes) == 1:
		if userNode.childNodes[0].nodeName != 'ID':
			raise Exception, 'xml format'
		user['userid'] = __getNodeText(userNode.childNodes[0].childNodes)
	elif len(userNode.childNodes) == 2:
		if userNode.childNodes[0].nodeName == 'ID' and userNode.childNodes[1].nodeName == 'DisplayName':
			user['userid'] = __getNodeText(userNode.childNodes[0].childNodes)
			user['username'] = __getNodeText(userNode.childNodes[1].childNodes)
		elif userNode.childNodes[1].nodeName == 'ID' and userNode.childNodes[0].nodeName == 'DisplayName':
			user['userid'] = __getNodeText(userNode.childNodes[1].childNodes)
			user['username'] = __getNodeText(userNode.childNodes[0].childNodes)
		else:
			raise Exception, 'xml format'
	else:
		raise Exception, 'xml format'
	return user

	
def __buildPermissionFromXML(permissionNode):
	permission = __getNodeText(permissionNode.childNodes)
	if permission not in ('READ', 'WRITE', 'READ_ACP', 'WRITE_ACP', 'FULL_CONTROL'):
		raise Exception, 'xml format'
	return permission


def __getNodeText(nodelist):
	rc = ""
	for node in nodelist:
		if node.nodeType == node.TEXT_NODE:
			rc = rc+ node.data
	return rc
