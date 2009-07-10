'''
Created on Jul 10, 2009

@author: Andrew
'''




def getServiceACP():
    """
    params:
        str user
    returns:
        str user
        str userDisplayName
        list ACP
            dict grant
                str grantee
                str granteeType
                str permission
    throws:
        InvalidUserName
        UserNotFound
        AccessDenied
    """


def setServiceACP():
    """
    params:
        str user
        list ACP
            dict grant
                str grantee
                str granteeType
                str permission
    throws:
        InvalidUserName
        UserNotFound
        AccessDenied
    """


def checkUserPermission():
    """
    params:
        str user
        str action
    returns:
        bool permitted
    throws:
        InvalidUserName
        UserNotFound
        InvalidAction
    """