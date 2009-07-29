'''
Created on Jul 10, 2009

@author: Andrew
'''

from utaka.src.DataAccess.connection import Connection

'''
params:
	str bucket
returns:
	{owner : {userid, username}, acl : [{grantee:{userid, username}, permission}]}
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
	str bucket
	accessControlPolicy: {owner : {userid, username}, acl : [{grantee:{userid, username}, permission}]}
		dict
			userid
			permission - 'read', 'write', 'read_acp', 'write_acp'
'''
def setBucketACP(bucket, accessControlPolicy):
	conn = Connection()
	removeString = 'delete from bucket_permission where bucket = %s'
	insertString = 'insert into bucket_permission (userid, bucket, permission) VALUES '
	aclWildcardList = []
	aclValueList = []
	for entry in accessControlPolicy['acl']:
		aclWildcardList.append('(%s, %s, %s)')
		aclValueList.append(entry['grantee']['userid'])
		aclValueList.append(bucket)
		aclValueList.append(entry['permission'])
	insertString += ', '.join(aclWildcardList)
	removeRS = conn.executeStatement(removeString, (bucket,))
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
	if action in ('write_log_status', 'read_log_status', 'destroy'):
		if not user:
			'''throw error'''
		conn = Connection()
		result = conn.executeStatement('select userid from bucket USING(userid) where userid = %s and bucket = %s', (user, bucket))
		conn.close()
		return len(result)
	elif action in ('read', 'write', 'read_acp', 'write_acp'):
		conn = Connection()
		if user:
			result = conn.executeStatement('select count(*) as rows from bucket_permission where userid IN(2, %s) and bucket = %s and permission IN(%s, "full_control")', (user, bucket, action))
		else:
			result = conn.executeStatement('select count(*) as rows from bucket_permission where userid = 1 and bucket = %s and permission IN(%s, "full_control")', (bucket, action))
		conn.close()
		return result[0][0] > 0
	else:
		'''throw error'''




