'''
Created on Jul 10, 2009

@author: Andrew
'''




def getObjectACP():
    """
    params:
        str key
        str bucket
        str user
    returns:
        str ownerId
        str ownerDisplayName
        list ACP
            dict grant
                str grantee
                str granteeType
                str permission
    throws:
        InvalidKeyName
        KeyNotFound
        InvalidBucketName
        BucketNotFound
        InvalidUserName
        UserNotFound
        AccessDenied
    """


def setObjectACP():
    """
    params:
        str key
        str bucket
        str user
        list ACP
            dict grant
                str grantee
                str granteeType
                str permission
    throws:
        InvalidKeyName
        KeyNotFound
        InvalidBucketName
        BucketNotFound
        InvalidUserName
        UserNotFound
        AccessDenied
    """        


def checkUserPermission():
    """
    params:
        str key
        str bucket
        str user
        str action
    returns:
        bool permitted
    throws:
        InvalidKeyName
        KeyNotFound
        InvalidBucketName
        BucketNotFound
        InvalidUserName
        UserNotFound
        InvalidAction
    """