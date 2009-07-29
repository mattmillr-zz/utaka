'''
Created on Jul 8, 2009

@author: Andrew
'''

from MySQLdb import escape_string
from utaka.src.DataAccess.connection import Connection
from utaka.src.errors.DataAccessErrors import UtakaDataAccessError
from utaka.src.errors.WriteErrors import UserWriteError
import hashlib
import time

def getService(userId):
    """
    parameters:
        int userId
    returns:
        dict
            dict user
                int userId
                str username
            dict buckets
                list
                    dict
                        str bucketName
                        str creationDate
    throws:
        InvalidUserName
        UserNotFound        
    """
    conn = Connection()
    query = "SELECT username FROM user WHERE userid = %s"
    result = conn.executeStatement(query, (int(userId)))
    if len(result) > 0:
        username = unicode(result[0][0], encoding='utf8')
    else:
        raise UtakaDataAccessError("UserNotFound")
    query = "SELECT bucket, bucket_creation_time FROM bucket WHERE userid = %s"
    result = conn.executeStatement(query, (userId))
    
    buckets = []
    for bucket in result:
        buckets.append({'bucketName':bucket[0],
                        'creationDate':str(bucket[1])})
    return {'user':{'userId':userId,'username':username},'buckets':buckets}

def setService(newUsername):
    """
    parameters:
        str newUsername
    throws
        InvalidUserName
    """
    conn = Connection()
    access = hashlib.sha1()
    secret = hashlib.sha1()
    access.update(str(newUsername))
    access.update(str(time.time()))
    secret.update(str(newUsername))
    success = False
    for i in range(3):
        access.update(str(secret.hexdigest()))
        access.update(str(time.time()))
        secret.update(str(time.time()))
        query = "SELECT COUNT(*) FROM user WHERE accesskey = %s OR secretkey = %s"
        count = conn.executeStatement(query, (str(access.hexdigest()), str(secret.hexdigest())))[0]
        if count == 0 and secret.hexdigest() != access.hexdigest():
            success = True
            break;
    
    if not success:
        raise UserWriteError("Unable to find unique authentication keys.")
    
    try:
        newUsername = unicode(escape_string(newUsername.encode('utf8')))
    except:
        newUsername = escape_string(str(newUsername))
    
    try:
        query = "INSERT INTO user (username, accesskey, secretkey) VALUES (%s, %s, %s)"
        conn.executeStatement(query, (newUsername, escape_string(str(access.hexdigest())), escape_string(str(secret.hexdigest()))))
    except:
        conn.cancelAndClose()
        raise UserWriteError("An error occured when creating the user.")
    
    conn.close()
    return (str(access.hexdigest()), str(secret.hexdigest()))

def copyService():
    """
    parameters:
        str user
        str newUser
    throws
        InvalidUserName
        UserNameTaken
    """


def destroyService():
    """
    parameters:
        str user
    throws
        InvalidUserName
        UserNotFound
    """

if __name__ == '__main__':
    print getService(3)