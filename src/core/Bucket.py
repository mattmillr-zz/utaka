'''
Created on Jul 8, 2009

@author: Andrew
'''

from MySQLdb import escape_string
from utaka.src.DataAccess.connection import Connection
from utaka.src.errors.BucketWriteErrors import BucketWriteError
from utaka.src.errors.DataAccessErrors import UtakaDataAccessError
from utaka.src.errors.InvalidDataErrors import *
import utaka.src.config as config
import os

def getBucket(bucket, userId, prefix, marker, maxKeys, delimiter):
    """
    params:
        str bucket
        int userId
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
    throws:
        InvalidBucket
        BucketNotFound
        UserNotFound
        InvalidArgument
    """
    #Check is the bucket name is valid
    (valid, rule) = _isValidBucketName(bucket)
    if valid == False:
        raise UtakaInvalidBucketError(rule)

    #Check if the bucket already exists
    conn = Connection()
    query = "SELECT userid FROM bucket WHERE bucket = %s"
    result = conn.executeStatement(query, (escape_string(str(bucket))))
    if len(result) == 0:
        raise UtakaDataAccessError("BucketNotFound")

    #Check if userid exists
    query = "SELECT username FROM user WHERE userid = %s"
    result = conn.executeStatement(query, (int(userId)))
    if len(result) == 0:
        raise UtakaDataAccessError("UserNotFound")

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
                            'lastModified':str(row[5]),
                            'eTag':str(row[4]),
                            'size':int(row[6]),
                            'storageClass':'STANDARD',
                            'owner':{'id':int(row[0]), 'name':unicode(row[7], encoding='utf8')}})
        else:
            commonPrefixes.append(str(row[9]))

    query = "SELECT COUNT(*) FROM object WHERE bucket = %s"
    count = conn.executeStatement(query, (escape_string(str(bucket))))[0][0]
    if count > len(contents):
        isTruncated = True
    else:
        isTruncated = False

    conn.close()

    return (contents, commonPrefixes, isTruncated)

def setBucket(bucket, userId):
    """
    params:
        str bucket
        int userId
    returns:
        void
    throws:
        BucketExists
        BucketExistsByUser
        InvalidBucket
        UserNotFound
        TooManyBuckets
        InvalidConfiguration
    """
    MAX_BUCKETS_PER_USER = 100

    #Check is the bucket name is valid
    (valid, rule) = _isValidBucketName(bucket)
    if valid == False:
        raise UtakaInvalidBucketError(rule)

    #Check if the bucket already exists
    conn = Connection()
    query = "SELECT userid FROM bucket WHERE bucket = %s"
    result = conn.executeStatement(query, (escape_string(str(bucket))))
    if len(result) > 0:
        if int(result[0][0]) == int(userId):
            raise BucketWriteError("BucketExistsByUser: You already created a bucket with that name.")
        else:
            raise BucketWriteError("BucketExists: That bucket already exists.")

    #Check if userid exists
    query = "SELECT username FROM user WHERE userid = %s"
    result = conn.executeStatement(query, (int(userId)))
    if len(result) == 0:
        raise UtakaDataAccessError("UserNotFound")

    #Check if user has too many buckets
    query = "SELECT bucket FROM bucket WHERE userid = %s"
    result = conn.executeStatement(query, (int(userId)))
    if len(result) >= MAX_BUCKETS_PER_USER:
        raise BucketWriteError("TooManyBuckets: You have reached the maximum number of buckets allowed per user.")

    #Write bucket to database and filesystem
    query = "INSERT INTO bucket (bucket, userid, bucket_creation_time) VALUES (%s, %s, NOW())"
    try:
        conn.executeStatement(query, (escape_string(str(bucket)), int(userId)))
    except:
        raise BucketWriteError("An error occured when creating the bucket.")
    path = config.get('common','filesystem_path')
    path += str(bucket)
    try:
        os.mkdir(path)
    except:
        conn.cancelAndClose()
        raise BucketWriteError("An error occured when creating the bucket.")
    conn.close()

def cloneBucket():
    """
    params:
        str sourceBucket
        str destinationBucket
        str user
    throws:
        InvalidBucketName
        BucketNotFound
        InvalidUserName
        UserNotFound
        TooManyBuckets
    """
    pass






def destroyBucket(bucket, userId):
    """
    params:
        str bucket
        int userId
    throws:
        BucketNotFound
        InvalidBucketName
        BucketNotEmpty
        UserNotFound
    """
    #Check is the bucket name is valid
    (valid, rule) = _isValidBucketName(bucket)
    if valid == False:
        raise UtakaInvalidBucketError(rule)

    #Check if the bucket already exists
    conn = Connection()
    query = "SELECT userid FROM bucket WHERE bucket = %s"
    result = conn.executeStatement(query, (escape_string(str(bucket))))
    if len(result) == 0:
        raise UtakaDataAccessError("BucketNotFound")

    #Check if userid exists
    query = "SELECT username FROM user WHERE userid = %s"
    result = conn.executeStatement(query, (int(userId)))
    if len(result) == 0:
        raise UtakaDataAccessError("UserNotFound")

    #Check if userid exists
    query = "SELECT COUNT(*) FROM object WHERE bucket = %s"
    result = conn.executeStatement(query, (escape_string(str(bucket))))
    if result[0][0] > 0:
        raise BucketWriteError("BucketNotEmpty")

    #Write bucket to database and filesystem
    query = "DELETE FROM bucket WHERE bucket = %s"
    try:
        conn.executeStatement(query, (escape_string(str(bucket))))
    except:
        raise BucketWriteError("An error occured when deleting the bucket.")
    path = config.get('common','filesystem_path')
    path += str(bucket)
    try:
        os.rmdir(path)
    except:
        conn.cancelAndClose()
        raise BucketWriteError("An error occured when deleting the bucket.")
    conn.close()

def _isValidBucketName(bucketName):
    import re
    reFaults = [r"[^a-z0-9\.-]",r"^[^a-z0-9]",r"^[a-z0-9\.-]{0,2}$",r"^[a-z0-9\.-]{64,}$",r"^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$",r"-$",r"(\.-|-\.)"]
    rules = ["Name must only contain lowercase letters, numbers, periods(.), and dashes(-).", "Name must only begin with a letter or number.",
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
    print "\n"