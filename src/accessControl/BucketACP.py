'''
Created on Jul 10, 2009

@author: Andrew
'''




def getBucketACP():    
    """
    params:
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
        InvalidBucketName
        BucketNotFound
        InvalidUserName
        UserNotFound
        AccessDenied
    """


def setBucketACP():
    """
    params:
        str bucket
        str user
        list ACP
            dict grant
                str grantee
                str granteeType
                str permission
    throws:
        InvalidBucketName
        BucketNotFound
        InvalidUserName
        UserNotFound
        AccessDenied
    """                


def checkUserPermission():
    """
    params:
        str user
        str bucket
        str action
    returns:
        bool permitted
    throws:
        InvalidBucketName
        BucketNotFound
        InvalidUserName
        UserNotFound
        InvalidAction
    """