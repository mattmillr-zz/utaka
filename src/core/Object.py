'''
Created on Jul 8, 2009

@author: Andrew
'''

def getObject():
    """
    params:
        str user
        str bucket
        str key
        bool getMetadata
        bool getData
        int byteRangeStart - optional
        int byteRangeEnd - optional
        str ifMatchTag - optional
        str ifNotMatchTag - optional    
        str ifModifiedSinceDate - optional
        str ifNotModifiedSinceDate - optional
        str ifRange - optional
    returns:
        str key
        str etag
        str lastModified
        dict metadata
        str data
        str content-type
        str content-disposition - conditional
        str content-range - conditional
        
    throws:
        InvalidKeyName
        InvalidBucketName
        InvalidUserName
        BucketNotFound
        UserNotFound
        KeyNotFound
        InvalidArgument?
        InvalidRange
        PreconditionFailed
    """
    pass

def setObject():
    """
    params:
        str key
        str bucket
        str user
        dict metadata
        str data
        content-type - optional
        content-disposition - optional
        content-md5 - optional
        content-encoding - optional
    returns:
        content-type
        etag
    throws:
        InvalidKeyName
        InvalidBucketName
        InvalidUserName
        BucketNotFound
        UserNotFound
    """
    pass

def cloneObject():
    """
    params:
        str sourceKey
        str sourceBucket
        str destinationKey
        str destinationBucket
        str user
        dict metadata - optional
        dict preconditions:
            str ifMatchTag
            str ifNotMatchTag
            str ifModifiedSinceDate
            str ifNotModifiedSinceDate
    throws:
        InvalidKeyName
        InvalidBucketName
        InvalidUserName
        KeyNotFound
        BucketNotFound
        UserNotFound
        PreconditionFailed        
    """
    pass

def destroyObject():
    """
    params:
        str key
        str bucket
        str user
    throws:
        InvalidKeyName
        InvalidBucketName
        InvalidUserName
        KeyNotFound
        BucketNotFound
        UserNotFound
    """
    pass