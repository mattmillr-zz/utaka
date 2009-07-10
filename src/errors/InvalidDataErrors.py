'''
Created on Jul 10, 2009

@author: Andrew
'''

import errors.UtakaErrors.UtakaError as UtakaError

class UtakaInvalidDataError(UtakaError):
    def __init__(self, msg):
        msg = "UtakaDataFormatError: " + msg
        UtakaError.__init__(self, msg)
        
class UtakaInvalidUserError(UtakaValidDataError):
    def __init__(self, msg):
        msg = "InvalidUser: " + msg
        UtakaValidDataError.__init__(self, msg)
        
class UtakaInvalidBucketError(UtakaValidDataError):
    def __init__(self, msg):
        msg = "InvalidBucket: " + msg
        UtakaValidDataError.__init__(self, msg)
        
class UtakaInvalidKeyError(UtakaValidDataError):
    def __init__(self, msg):
        msg = "InvalidKey: " + msg
        UtakaValidDataError.__init__(self, msg)
        
class UtakaInvalidArgumentError(UtakaValidDataError):
    def __init__(self, msg):
        msg = "InvalidArgument: " + msg
        UtakaValidDataError.__init__(self, msg)

class UtakaInvalidConfigurationError(UtakaValidDataError):
    def __init__(self, msg):
        msg = "InvalidConfiguration: " + msg
        UtakaValidDataError.__init__(self, msg)