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

from MySQLdb import escape_string
from utaka.src.dataAccess.Connection import Connection
import utaka.src.exceptions.BadRequestException as BadRequestException
import utaka.src.exceptions.ConflictException as ConflictException
import utaka.src.exceptions.NotFoundException as NotFoundException

import utaka.src.Config as Config
import os


'''
getBucket
	params:
		str bucket
		str prefix
		str marker
		int maxKeys
		str delimiter
	returns:
		tuple
			list contents
				dict vals
				str key
				str lastModified
				str eTag
				int size
				str storageClass
				dict owner
				int id
				str name
				list commonPrefixes
					str prefix
'''
def getBucket(bucket, prefix, marker, maxKeys, delimiter):
	'''returns listing of objects inside a bucket'''
	conn = Connection()
	try:
		#Validate the bucket
		_verifyBucket(conn, bucket, True)

		#get objects
		group = False
		if prefix != None:
			if delimiter != None and delimiter != "":
				delimiter = escape_string(str(delimiter))
				count = prefix.count(delimiter) + 1
				queryGroup = " GROUP BY SUBSTRING_INDEX(o.object, '"+delimiter+"', "+str(count)+")"
				group = True
				query = "SELECT o.userid, o.object, o.bucket, o.object_create_time, o.eTag, o.object_mod_time, o.size, u.username, COUNT(*), CONCAT(SUBSTRING_INDEX(o.object, '"+delimiter+"', "+str(count)+"), '"+delimiter+"') FROM object as o, user as u WHERE o.bucket = %s AND o.userid = u.userid"
			else:
				query = "SELECT o.userid, o.object, o.bucket, o.object_create_time, o.eTag, o.object_mod_time, o.size, u.username, 1 FROM object as o, user as u WHERE o.bucket = %s AND o.userid = u.userid"
				prefix = escape_string(str(prefix))
				prefix.replace('%','%%')
				prefix += '%'
				query += " AND o.object LIKE %s"
		else:
			query = "SELECT o.userid, o.object, o.bucket, o.object_create_time, o.eTag, o.object_mod_time, o.size, u.username, 1 FROM object as o, user as u WHERE o.bucket = %s AND o.userid = u.userid"

		if marker != None:
			marker = escape_string(str(marker))
			query += " AND STRCMP(o.object, '"+marker+"') > 0"

		if group == True:
			query += queryGroup
		else:
			query += " ORDER BY o.object"

		if maxKeys and int(maxKeys) > -1:
			query += " LIMIT "+str(int(maxKeys))

		if prefix != None:
			print (query % ("'%s'", "'%s'")) % (escape_string(str(bucket)), prefix)
			result = conn.executeStatement(query, (escape_string(str(bucket)), prefix))
		else:
			print (query % ("'%s'")) % (escape_string(str(bucket)))
			result = conn.executeStatement(query, (escape_string(str(bucket))))

		contents = []
		commonPrefixes = []
		for row in result:
			if int(row[8]) == 1:
				contents.append({'key':str(row[1]),
				                 'lastModified':((row[5]).isoformat('T') + 'Z'),
				                 'eTag':str(row[4]),
				                 'size':int(row[6]),
				                 'storageClass':'STANDARD',
				                 'owner':{'id':int(row[0]),
				                 'name':unicode(row[7], encoding='utf8')}})
			else:
				commonPrefixes.append(str(row[9]))

		query = "SELECT COUNT(*) FROM object WHERE bucket = %s"
		count = conn.executeStatement(query, (escape_string(str(bucket))))[0][0]
		if count > len(contents):
			isTruncated = True
		else:
			isTruncated = False
	except:
		conn.cancelAndClose()
		raise
	conn.close()
	return (contents, commonPrefixes, isTruncated)





'''
setBucket
	params:
		str bucket
		int userid
'''
def setBucket(bucket, userid):
	'''creates a new empty bucket'''
	MAX_BUCKETS_PER_USER = 100

	conn = Connection()
	#Validate the bucket
	try:
		_verifyBucket(conn, bucket, False, userid)

		#Check if user has too many buckets
		query = "SELECT bucket FROM bucket WHERE userid = %s"
		result = conn.executeStatement(query, (int(userid)))
		if len(result) >= MAX_BUCKETS_PER_USER:
				raise BadRequestException.TooManyBucketsException()

		#Write bucket to database and filesystem
		query = "INSERT INTO bucket (bucket, userid, bucket_creation_time) VALUES (%s, %s, NOW())"
		conn.executeStatement(query, (escape_string(str(bucket)), int(userid)))
		path = Config.get('common','filesystem_path')
		path += str(bucket)
		os.mkdir(path)
	except:
		conn.cancelAndClose()
		raise
	else:
		conn.close()





'''
cloneBucket
	params:
		str sourceBucket
		str destinationBucket
		str userid
'''
def cloneBucket(sourceBucket, destinationBucket, userid):
	'''makes a deep copy of a bucket'''
	pass


'''
destroyBucket
	params:
		str bucket
'''
def destroyBucket(bucket):
	'''destroys a bucket if empty'''
	conn = Connection()
	try:
		#Validate the bucket
		_verifyBucket(conn, bucket, True)

		#Check if the bucket is empty
		query = "SELECT COUNT(*) FROM object WHERE bucket = %s"
		result = conn.executeStatement(query, (escape_string(str(bucket))))
		if result[0][0] > 0:
			raise ConflictException.BucketNotEmptyException(bucket)

		#Delete the bucket from the database and the filesystem
		query = "DELETE FROM bucket WHERE bucket = %s"
		conn.executeStatement(query, (escape_string(str(bucket))))
		path = Config.get('common','filesystem_path')
		path += str(bucket)
		os.rmdir(path)
	except:
		conn.cancelAndClose()
		raise
	else:
		conn.close()


'''
_verifyBucket
	params:
		conn
		bucketName
		userid
		exists
	returns:
'''
def _verifyBucket(conn, bucketName, exists, userid=None):
	'''verifies if a bucketname is valid and can if it exists'''
	#Check is the bucket name is valid
	(valid, rule) = _isValidBucketName(bucketName)
	if valid == False:
		raise BadRequestException.InvalidBucketNameException(bucketName)
	#Check whether or not the bucket exists
	query = "SELECT userid FROM bucket WHERE bucket = %s"
	result = conn.executeStatement(query, (escape_string(str(bucketName))))
	if len(result) > 0 and exists == False:
		if userid and (int(result[0][0]) == int(userid)):
			raise ConflictException.BucketAlreadyOwnedByYouException(bucketName)
		else:
			raise ConflictException.BucketAlreadyExistsException(bucketName)
	elif len(result) == 0 and exists == True:
			raise NotFoundException.NoSuchBucketException(bucketName)


'''
_isValidBucketName
	params:
		bucketName
	returns:
		bool isValid
'''
def _isValidBucketName(bucketName):
	'''verifies a valid bucketname'''
	import re
	reFaults = [r"[^a-zA-Z0-9\.-]",r"^[^a-zA-Z0-9]",r"^[a-zA-Z0-9\.-]{0,2}$",r"^[a-zA-Z0-9\.-]{64,}$",r"^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$",r"-$",r"(\.-|-\.)"]
	rules = ["Name must contain only letters, numbers, periods(.), and dashes(-).", "Name must only begin with a letter or number.",
	         "Name must be 3 to 63 characters long.", "Name must be 3 to 63 characters long.", "Name must not be in ip address style (e.g. 127.0.0.1).",
	         "Name must not end with a dash(-).", "Name must not have an adjacent period(.) and dash(-) (e.g. .- or -.)."]
	valid = True
	rule = ""
	print bucketName
	for index, expression in enumerate(reFaults):
		match = re.search(expression, str(bucketName))
		if match != None:
			valid = False
			#print expression
			rule = rules[index]
			break
	return valid, rule





if __name__ == '__main__':
    print "\n"
    try:
        print setBucket('bil\nlt', 3) #true
    except Exception, e:
        print str(e)
    """print "\n"
    try:
        print setBucket('billt', 3) #true
    except Exception, e:
        print str(e)
    print "\n"
    try:
        print setBucket('b-t.', 3) #true
    except Exception, e:
        print str(e)
    print "\n"
    try:
        print setBucket('b-t.test', 3) #true
    except Exception, e:
        print str(e)
    print "\n"
    try:
        print setBucket('billt.test', 3) #true
    except Exception, e:
        print str(e)
    print "\n"
    try:
        print setBucket('a-5', 3) #true
    except Exception, e:
        print str(e)
    print "\n"
    try:
        print setBucket('wierd$#&@^()^', 3) #false
    except Exception, e:
        print str(e)
    print "\n"
    try:
        print setBucket('-asdd', 3) #false
    except Exception, e:
        print str(e)
    print "\n"
    try:
        print setBucket('10.10.11.185', 3) #false
    except Exception, e:
        print str(e)
    print "\n"
    try:
        print setBucket('a____', 3) #false
    except Exception, e:
        print str(e)
    print "\n"
    try:
        print setBucket('sh', 3) #false
    except Exception, e:
        print str(e)
    print "\n"
    try:
        print setBucket('1234567890123456789012345678901234567890123456789012345678901234567890', 3) #false
    except Exception, e:
        print str(e)
    print "\n"
    try:
        print setBucket('billt-', 3) #false
    except Exception, e:
        print str(e)
    print "\n"
    try:
        print setBucket('bi.-t', 3) #false
    except Exception, e:
        print str(e)
    print "\n"
    try:
        print setBucket('bi-.t', 3) #false
    except Exception, e:
        print str(e)
    print "\n"
    try:
        print getBucket('billt', 3, '/', None, -1, '/')
    except Exception, e:
        print str(e)
    print "\n"
    try:
        print getBucket('billt', 3, '/First/', None, -1, '/')
    except Exception, e:
        print str(e)
    print "\n"
    try:
        print getBucket('billt', 3, None, None, -1, None)
    except Exception, e:
        print str(e)
    print "\n"
    try:
        print getBucket('billt', 3, None, None, 5, None)
    except Exception, e:
        print str(e)
    print "\n"
    try:
        print destroyBucket('b-t.', 3) #true
    except Exception, e:
        print str(e)
    print "\n"
    try:
        print destroyBucket('b-t.test', 3) #true
    except Exception, e:
        print str(e)
    print "\n" """