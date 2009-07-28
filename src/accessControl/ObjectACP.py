'''
Created on Jul 10, 2009
 edited Jul 26, 2009
@author: Andrew
'''

from utaka.src.DataAccess.connection import Connection

'''
params:
	bucket
	key
returns:
	list of dictionaries with userid, username, and permission fields with first row being owner
'''
def getObjectACP(bucket, key):
	conn = Connection(useDictCursor = True)
	rs = conn.executeStatement('''SELECT userid, username, 'owner' as permission
	                              FROM user JOIN object USING(userid)
	                              WHERE object = %s and bucket = %s
	                              UNION
	                              SELECT userid, username, permission
	                              FROM object_permission JOIN user USING(userid)
	                              WHERE object = %s and bucket = %s''', (key, bucket, key, bucket))
	conn.close()
	return rs
 
'''
params:
	bucket
	key
	list of dictionaries with userid, permission fields
'''
def setObjectACP(bucket, key, accessControlList):
	conn = Connection()
	removeString = 'delete from object_permission where bucket = %s and object = %s'
	insertString = 'insert into object_permission (userid, bucket, object, permission) VALUES'
	aclWildcardList = []
	aclValueList = []
	for entry in accessControlList:
		aclWildcardList.append('(%s, %s, %s, %s)')
		aclValueList.append(entry['userid'])
		aclValueList.append(bucket)
		aclValueList.append(key)
		aclValueList.append(entry['permission'])
	insertString += ', '.join(aclWildcardList)
	removeRS = conn.executeStatement(deleteString, (bucket, object))
	insertRS = conn.executeStatement(insertString, aclValueList)
	conn.close()
 
 
'''
params:
	key
	bucket
	user
	action
returns:
	bool permitted
'''
def checkUserPermission(user, bucket, key, action):
	if action == 'get':
		permission = 'read'
	elif action == 'set':
		permission = 'write'
	elif action == 'get_acp':
		permission = 'read_acp'
	elif action == 'set_acp':
		permission = 'write_acp'
	else:
		'''throw error'''
	conn = Connection()
	if user:
		result = conn.executeStatement('select count(*) as rows from object_permission where userid IN(2, %s) and object = %s and bucket = %s and permission = %s', (user, key, bucket, permission))
	else:
		result = conn.executeStatement('select count(*) as rows from object_permission where userid = 1 and object = %s and bucket = %s and permission = %s', (key, bucket, permission))
	conn.close()
	return result[0][0] > 0