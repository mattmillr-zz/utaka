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
	{owner : {userid, username}, acl : [{grantee:{userid, username}, permission}]}
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
	acp = {}
	if len(rs) > 0:
		acp['owner'] = {'userid':rs[0]['userid'], 'username':rs[0]['username']}
		acp['acl'] = []
		for grant in rs[1:]:
			acp['acl'].append({'grantee':{'userid':grant['userid'], 'username':grant['username']}, 'permission':grant['permission']})
	else:
		raise Exception, 'object not found'
	return acp


'''
params:
	bucket
	key
	accessControlPolicy: {owner : {userid, username}, acl : [{grantee:{userid, username}, permission}]}
'''
def setObjectACP(bucket, key, accessControlPolicy):
	conn = Connection()
	removeString = 'delete from object_permission where bucket = %s and object = %s'
	insertString = 'insert into object_permission (userid, bucket, object, permission) VALUES'
	aclWildcardList = []
	aclValueList = []
	for entry in accessControlPolicy['acl']:
		aclWildcardList.append('(%s, %s, %s, %s)')
		aclValueList.append(entry['grantee']['userid'])
		aclValueList.append(bucket)
		aclValueList.append(key)
		aclValueList.append(entry['permission'])
	insertString += ', '.join(aclWildcardList)
	removeRS = conn.executeStatement(removeString, (bucket, key))
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
	if action in ('read', 'read_acp', 'write_acp'):
		conn = Connection()
		if user:
			result = conn.executeStatement('select count(*) as rows from object_permission where userid IN(2, %s) and object = %s and bucket = %s and permission IN(%s, "full_control")', (user, key, bucket, action))
		else:
			result = conn.executeStatement('select count(*) as rows from object_permission where userid = 1 and object = %s and bucket = %s and permission IN(%s, "full_control")', (key, bucket, action))
		conn.close()
		return result[0][0] > 0
	elif action in('write'):
		conn = Connection()
		if user:
			result = conn.executeStatement('''SELECT SUM( (SELECT COUNT(*) FROM bucket_permission where userid IN(2, %s) and bucket = %s and permission IN('write', 'full_control')
			          + (SELECT COUNT(*) FROM object_permission where userid IN(2, %s) and bucket = %s and object = %s and permission IN('write', 'full_control'))''', (user, bucket, user, bucket, object))
		else:
			result = conn.executeStatement('''SELECT SUM( (SELECT COUNT(*) FROM bucket_permission where userid = 1 and bucket = %s and permission IN('write', 'full_control')
			          + (SELECT COUNT(*) FROM object_permission where userid = 1 and bucket = %s and object = %s and permission IN('write', 'full_control'))''', (bucket, bucket, object))
		conn.close()
		return result[0][0] > 0
	else:
		raise exception, "Invalid action"