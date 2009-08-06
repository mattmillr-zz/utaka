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
import utaka.src.exceptions.BadRequestException as BadRequestException

'''
getService
	params:
	returns:
'''
def getService(userid):
	'''returns list of buckets owned by user'''
	conn = Connection(True)
	try:
		result = conn.executeStatement("SELECT bucket, bucket_creation_time, username FROM bucket RIGHT JOIN user USING(userid) WHERE userid = %s", (userid,))
	except:
		conn.cancelAndClose()
		raise
	else:
		conn.close()
	buckets = []
	for bucket in result:
		if bucket['bucket'] != None:
			buckets.append({'bucketName':bucket['bucket'], 'creationDate':((bucket['bucket_creation_time']).isoformat('T') + 'Z')})
	return {'user':{'userid':userid,'username':result[0]['username']},'buckets':buckets}

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
	userid
'''
def destroyService(userid):
	'''deletes an owner'''
	if not userid or userid <3:
		raise BadRequestExceptin.UseridNotValidException(userid)
	conn = Connection()
	try:
		#Check if user exists
		checkUserResult = conn.executeStatement('select count(*) from user where userid = %s', (userid,))
		if checkUserResult[0][0] == 0:
			raise BadRequestException.UseridNotFoundException(userid)
		#Give ownership of existing objects to enclosing bucket owners
		conn.executeStatement('update object, bucket set object.userid = bucket.userid where object.bucket = bucket.bucket and object.userid = %s', (userid,))
		#Empty existing buckets
		conn.executeStatement('delete from object where userid = %s', (userid,))
		#Delete buckets
		conn.executeStatement('delete from bucket where userid = %s', (userid,))
		#Delete user
		conn.executeStatement('delete from user where userid = %s', (userid,))
	except:
		conn.cancelAndClose()
		raise
	conn.close()

if __name__ == '__main__':
		print getService(3)