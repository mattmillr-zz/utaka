'''
Created on Jul 10, 2009

@author: Andrew
'''

from utaka.src.DataAccess.connection import Connection

'''
params:
	str bucket
returns:
	list of dictionaries with userid, username, and permission fields, first row being owner
'''
def getBucketACP(bucket):
	conn = Connection(useDictCursor = True)
	rs = conn.executeStatement('''SELECT userid, username, 'owner' as permission
	                              FROM user JOIN bucket USING(userid) WHERE bucket = %s
	                              UNION
	                              SELECT userid, username, permission
	                              FROM bucket_permission JOIN user USING(userid)
	                              WHERE bucket = %s''', (bucket, bucket))
	conn.close()
	return rs


'''
params:
	str bucket
	list accessControlList
		dict
			userid
			permission - 'read', 'write', 'read_acp', 'write_acp'
'''
def setBucketACP(bucket, accessControlList):
	conn = Connection()
	removeString = 'delete from bucket_permission where bucket = %s'
	insertString = 'insert into bucket_permission (userid, bucket, permission) VALUES '
	aclWildcardList = []
	aclValueList = []
	for entry in accessControlList:
		aclWildcardList.append('(%s, %s, %s)')
		aclValueList.append(entry['userid'])
		aclValueList.append(bucket)
		aclValueList.append(entry['permission'])
	insertString += ', '.join(aclWildcardList)
	removeRS = conn.executeStatement(deleteString, (bucket,))
	insertRS = conn.executeStatement(insertString, aclValueList)
	conn.close()


'''
params:
	user
	bucket
	action
returns:
	bool permitted
'''
def checkUserPermission(user, bucket, action):
	if action == 'write':
		return user
	elif action == 'write_log_status' or action == 'read_log_status':
		if not user:
			'''throw error'''
		conn = Connection()
		result = conn.executeStatement('select userid from user join bucket USING(userid) where userid = %s and bucket = %s', (user, bucket))
		conn.close()
		return len(result)
		
		'''check if user is owner of bucket'''
	elif action not in ('read', 'read_acp', 'write_acp'):
		'''throw error'''
	else:
		conn = Connection()
		if user:
			result = conn.executeStatement('select count(*) as rows from bucket_permission where userid IN(2, %s) and bucket = %s and permission = %s', (user, bucket, action))
		else:
			result = conn.executeStatement('select count(*) as rows from bucket_permission where userid = 1 and bucket = %s and permission = %s', (bucket, action))
		conn.close()
		return result[0][0] > 0




