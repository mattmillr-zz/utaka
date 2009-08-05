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


from utaka.src.dataAccess.Connection import Connection
import utaka.src.exceptions.InternalErrorException as InternalErrorException

'''
getService
	params:
	returns:
'''
def getService(userId):
	'''returns list of buckets owned by user'''
	conn = Connection(True)
	try:
		query = "SELECT bucket, bucket_creation_time, username FROM bucket RIGHT JOIN user USING(userid) WHERE userid = %s"
		result = conn.executeStatement(query, (userId,))
	except:
		conn.cancelAndClose()
		raise
	else:
		conn.close()
	buckets = []
	for bucket in result:
		if bucket['bucket'] != None:
			buckets.append({'bucketName':bucket['bucket'], 'creationDate':str(bucket['bucket_creation_time'])})
	return {'user':{'userId':userId,'username':result[0]['username']},'buckets':buckets}

'''
setService
	params:
	returns:
'''
def setService(username, isAdmin=False):
	'''adds new user'''
	conn = Connection()
	try:
		import random
		import hashlib
		access = hashlib.sha1()
		secret = hashlib.sha1()
		access.update(username + str(random.getrandbits(16)))
		secret.update(str(random.getrandbits(16)) + username)
		accessHexDigest = access.hexdigest()
		secretHexDigest = secret.hexdigest()
		success = False
		for i in range(3):
			try:
				conn.executeStatement('insert into user(username, accesskey, secretkey, isAdmin) values(%s, %s, %s, %s)', (username, accessHexDigest, secretHexDigest, bool(isAdmin)))
			except InternalErrorException.DatabaseIntegrityErrorException:
				access.update(str(random.getrandbits(16)))
				secret.update(str(random.getrandbits(16)))
				accessHexDigest = access.hexdigest()
				secretHexDigest = secret.hexdigest()
			else:
				success = True
				break
		if not success:
			raise InternalErrorException.KeyCollisionErrorException()
	except:
		conn.cancelAndClose()
		raise
	else:
		conn.close()
	return (accessHexDigest, secretHexDigest)

def copyService():
	pass

'''
destroyService
params:
	userId
'''
def destroyService(userId):
	'''deletes an owner'''
	conn = Connection()
	try:
		#Check if user exists
		checkUserResult = conn.executeStatment('select count(*) from user where userid = %s', (userId,))
		if conn.getRowCount() == 0:
			'''raise error'''
		#Give ownership of existing objects to enclosing bucket owners

		query = "SELECT bucket, object FROM object WHERE userid = %s"
		result = conn.executeStatement(query, (int(userId)))
		query = "UPDATE object SET userid = (SELECT userid FROM bucket WHERE bucket = %s) WHERE bucket = %s AND object = %s"
		for row in result:
			conn.executeStatement(query, (escape_string(str(row[0])), escape_string(str(row[0])), escape_string(str(row[1]))))

		#Check if user still has objects
		query = "SELECT COUNT(*) FROM object WHERE userid = %s"
		count = conn.executeStatement(query, (int(userId)))[0]
		if count > 0:
			raise UserWriteError("User still has objects.")

		#Check if user still has buckets
		query = "SELECT COUNT(*) FROM bucket WHERE userid = %s"
		count = conn.executeStatement(query, (int(userId)))[0]
		if count > 0:
			raise UserWriteError("User still has buckets.")

		#Delete permissions pertaining to user
		conn.executeStatement(query, (int(userId)))
		query = "DELETE FROM object_permission WHERE userid = %s"
		conn.executeStatement(query, (int(userId)))

		#Delete user
		query = "DELETE FROM user WHERE userid = %s"
		conn.executeStatement(query, (int(userId)))
	except:
		conn.cancelAndClose()
		raise
	conn.close()

if __name__ == '__main__':
		print getService(3)