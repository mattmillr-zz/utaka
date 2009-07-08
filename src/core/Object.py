'''
Created on Jul 8, 2009

@author: Andrew
'''


def createObject():
    """
    LOOK UP 100-continue
            cache-control
    params:
        str bucket
        str key
        dict authorization
        cache-control - optional 
        content-length
        content-type - optional
        content-disposition - optional
        content-md5 - optional
        content-encoding - optional
        acl - optional
        metadata - optional
    returns:
        content-type
        etag
        
        
        
        
        
        
    """
    pass

def destroyObject():
    """
    
    """
    pass

def getObject():
    """
    params:
        str bucket
        str key
        dict authorization:
        bool getMetadata
        bool getData
        int byteRangeStart - optional
        int byteRangeEnd - optional
        dict preconditionals:
            str ifMatchTag - optional
            str ifNotMatchTag - optional    
            str ifModifiedSinceDate - optional
            str ifNotModifiedSinceDate - optional
    returns:
        str key
        str etag
        str lastModified
        str content-type
        str content-disposition - optional
        str content-length - conditional
        str content-range - conditional
        dict metadata
        bytestream? data
        
    throws:
        AccessDenied
        InvalidAccessKeyId
        InvalidArgument?
        InvalidBucketName
        InvalidRange
        NoSuchBucket
        NoSuchKey
        PreconditionFailed
        SignatureDoesNotMatch         
    """
    pass

def cloneObject():
    """
    
    """
    pass

def getObjectACP():
    """
    params:
        str bucket
        str key
        
    """
    pass

def setObjectACP():
    """
    params:
    str key
    
    """
    pass
    