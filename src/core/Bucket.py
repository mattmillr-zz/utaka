'''
Created on Jul 8, 2009

@author: Andrew
'''

from MySQLdb import escape_string
from Utaka.src.DataAccess.connection import Connection
from Utaka.src.errors.BucketWriteErrors import BucketWriteError
from Utaka.src.errors.DataAccessErrors import UtakaDataAccessError
from Utaka.src.errors.InvalidDataErrors import *

def getBucket():
    """
    params:
        str bucket
        str user
        str prefix
        str marker
        str maxKeys
        str delimiter
    returns:
        list contents
            dict vals
                str key
                str lastModified
                str eTag
                int size
                str storageClass
                str user
                str userCommon
    throws:
        InvalidBucketName
        BucketNotFound
        InvalidUserName
        UserNotFound
        InvalidArgument
    """
    pass



def setBucket(bucket, userId, configurations):
    """
    params:
        str bucket
        int userId
        dict configurations
    returns:
        void
    throws:
        BucketExists
        BucketExistsByUser
        InvalidBucketName
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
    
    #Check configurations
    
    #Write bucket to database and filesystem
    
    #Write configurations to database

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






def destroyBucket():    
    """ 
    params:
        str bucket
        str user
    throws:
        BucketNotFound
        InvalidBucketName
        BucketNotEmpty
        UserNotFound
    """
    pass


def _isValidBucketName(bucketName):
    import re
    reFaults = [r"[^a-zA-Z0-9\.-]",r"^[^a-zA-Z0-9]",r"^[a-zA-Z0-9\.-]{0,2}$",r"^[a-zA-Z0-9\.-]{64,}$",r"^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$",r"-$",r"(\.-|-\.)"]
    rules = ["Name must only contain letters, numbers, periods(.), and dashes(-).", "Name must only begin with a letter or number.", "Name must be 3 to 63 characters long.",
            "Name must be 3 to 63 characters long.", "Name must not be in ip address style (e.g. 127.0.0.1).", "Name must not end with a dash(-).",
            "Name must not have an adjacent period(.) and dash(-) (e.g. .- or -.)."]
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
    try:
        print setBucket('billt') #true
    except UtakaInvalidBucketError, e:
        print str(e)
    try:
        print setBucket('b-t.') #true
    except UtakaInvalidBucketError, e:
        print str(e)
    try:
        print setBucket('wierd$#&@^()^') #false
    except UtakaInvalidBucketError, e:
        print str(e)
    try:
        print setBucket('-asdd') #false
    except UtakaInvalidBucketError, e:
        print str(e)
    try:
        print setBucket('10.10.11.185') #false
    except UtakaInvalidBucketError, e:
        print str(e)
    try:
        print setBucket('a____') #false
    except UtakaInvalidBucketError, e:
        print str(e)
    try:
        print setBucket('sh') #false
    except UtakaInvalidBucketError, e:
        print str(e)
    try:
        print setBucket('1234567890123456789012345678901234567890123456789012345678901234567890') #false
    except UtakaInvalidBucketError, e:
        print str(e)
    try:
        print setBucket('billt-') #false
    except UtakaInvalidBucketError, e:
        print str(e)
    try:
        print setBucket('bi.-t') #false
    except UtakaInvalidBucketError, e:
        print str(e)
    try:
        print setBucket('bi-.t') #false
    except UtakaInvalidBucketError, e:
        print str(e)