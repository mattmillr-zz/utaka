'''
Created on Jul 8, 2009

@author: Andrew
'''

from MySQLdb import escape_string
from utaka.src.DataAccess.connection import Connection
from utaka.src.errors.DataAccessErrors import UtakaDataAccessError

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

def setService():
    """
    parameters:
        str user
    throws
        InvalidUserName
        UserNameTaken
    """    


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