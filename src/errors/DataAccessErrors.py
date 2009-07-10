'''
Created on Jul 10, 2009

@author: Andrew
'''




import errors.UtakaErrors.UtakaError as UtakaError

class UtakaDataAccessError(UtakaError):
    def __init__(self, msg):
        msg = "UtakaDataAccessError: " + msg
        UtakaError.__init__(self, msg)