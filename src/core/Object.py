'''
Created on Jul 8, 2009

@author: Andrew
'''


def createObject():
    """
    
    """
    pass

def destroyObject():
    """
    
    """
    pass

def getObject():
    """
    params:
        str key
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
        data
        
    throws: precondition failed, not modified,  
    """
    pass

def cloneObject():
    """
    
    """
    pass

def getObjectACP():
    """
    
    """
    pass

def setObjectACP():
    """
    params:
    str key
    
    """
    pass
    