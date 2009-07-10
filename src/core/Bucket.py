'''
Created on Jul 8, 2009

@author: Andrew
'''




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



def setBucket():
    """
    params:
        str bucket
        str user
        dict configurations
    returns:
        void
    throws:
        BucketExists
        BucketExistsByUser
        InvalidBucketName
        UserNotFound
        InvalidUserName
        TooManyBuckets
        InvalidConfiguration
    """    
    pass


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



