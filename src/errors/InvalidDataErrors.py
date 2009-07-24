'''
Created on Jul 10, 2009

@author: Andrew
'''

from utaka.src.errors.UtakaErrors import UtakaError

class UtakaInvalidDataError(UtakaError):
    def __init__(self, msg):
        msg = "UtakaDataFormatError: " + msg
        UtakaError.__init__(self, msg)
        
class UtakaInvalidUserError(UtakaInvalidDataError):
    def __init__(self, msg):
        msg = "InvalidUser: " + msg
        UtakaInvalidDataError.__init__(self, msg)
        
class UtakaInvalidBucketError(UtakaInvalidDataError):
    def __init__(self, msg):
        msg = "InvalidBucket: " + msg
        UtakaInvalidDataError.__init__(self, msg)
        
class UtakaInvalidKeyError(UtakaInvalidDataError):
    def __init__(self, msg):
        msg = "InvalidKey: " + msg
        UtakaInvalidDataError.__init__(self, msg)
        
class UtakaInvalidArgumentError(UtakaInvalidDataError):
    def __init__(self, msg):
        msg = "InvalidArgument: " + msg
        UtakaInvalidDataError.__init__(self, msg)

class UtakaInvalidConfigurationError(UtakaInvalidDataError):
    def __init__(self, msg):
        msg = "InvalidConfiguration: " + msg
        UtakaInvalidDataError.__init__(self, msg)