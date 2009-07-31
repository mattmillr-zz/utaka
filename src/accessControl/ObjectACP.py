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
	rs = conn.executeStatement(
	  '''SELECT userid, username, 'owner' as permission
	     FROM user JOIN object USING(userid)
	     WHERE object = %s and bucket = %s
	     UNION
	     SELECT userid, username, permission
	     FROM object_permission JOIN user USING(userid)
	     WHERE object = %s and bucket = %s
	  ''', (key, bucket, key, bucket))
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
raises:
	NoSuchKeyException, InternalErrorException
'''
def checkUserPermission(user, bucket, key, action):
	if action in ('read', 'read_acp', 'write_acp'):
		conn = Connection()
		if user:
			result = conn.executeStatement(
			  '''SELECT (SELECT COUNT(*) from object WHERE bucket = %s and object = %s) + 
			    (SELECT COUNT(*) from object_permission
			     WHERE bucket = %s and object = %s and userid = %s and permission IN(%s, 'full_control'))
			  ''', (bucket, object, bucket, object, userid, action))
		else:
			result = conn.executeStatement(
			  '''SELECT (SELECT COUNT(*) FROM object WHERE bucket = %s and object = %s) + 
			    (SELECT COUNT(*) FROM object_permission WHERE bucket = %s and object = %s and userid = 1 and permission IN(%s, 'full_control'))
			  ''', (bucket, object, bucket, object, action))
		conn.close()
		if result[0][0] == 0:
			raise NotFoundException.NoSuchKeyException(bucket, key)
		else:
			return result[0][0] > 1
	elif action in('write'):
		conn = Connection()
		if user:
			result = conn.executeStatement(
			  '''SELECT ( SELECT COUNT(*) FROM object WHERE bucket = %s and object = %s ) +
			    (SELECT COUNT(*) FROM bucket_permission where userid IN(2, %s) and bucket = %s and permission IN('write', 'full_control')) +
			    (SELECT COUNT(*) FROM object_permission where userid IN(2, %s) and bucket = %s and object = %s and permission IN('write', 'full_control'))
			  ''', (bucket, key, user, bucket, user, bucket, key))
		else:
			result = conn.executeStatement(
			  '''SELECT ( SELECT COUNT(*) FROM object WHERE bucket = %s and object = %s ) +
			    (SELECT COUNT(*) FROM bucket_permission where userid = 1 and bucket = %s and permission IN('write', 'full_control')) +
			    (SELECT COUNT(*) FROM object_permission where userid = 1 and bucket = %s and object = %s and permission IN('write', 'full_control'))
			  ''', (bucket, key, bucket, bucket, key))
		conn.close()
		if result[0][0] == 0:
			raise NotFoundException.NoSuchKeyException(bucket, key)
		else:
			return result[0][0] > 1
	else:
		raise InternalErrorException.BadArgumentException('action', str(action),
		  'Invalid action for ObjectACP.checkUserPermission: action must be IN ("write", "read", "write_acp", "read_acp").')
