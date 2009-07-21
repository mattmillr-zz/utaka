'''
Created on Jul 21, 2009

@author: Andrew
'''

from mod_python import apache
from Utaka.RestResources.HMAC_SHA1_Authentication import getUser

class UtakaRequest:

    def __init__(self, req, virtualBucket=False):
        self.req = req
        self.bucket = self.key = None
        self.srLogging = self.srACL = self.srTorrent = self.srLocation = False
        self.method = self.req.method
        
        #Query string digest
        if self.req.args:
            subresources = util.parse_qs(self.req.args, True)
            self.srLogging = 'logging' in subresources
            self.srACL = 'acl' in subresources
            self.srTorrent = 'torrent' in subresources
            self.srLocation = 'location' in subresources
            if self.srLogging:
                if self.srACL or self.srTorrent or self.srLocation:
                    '''throw error'''
            elif self.srACL:
                if self.srTorrent or self.srLocation:
                    '''throw error'''
            elif self.srTorrent:
                if self.srLocation:
                    '''throw error'''

        #URI digest
        splitURI = req.uri.split('/', 2)
        for segment in splitURI[:]:
            if len(segment) == 0:
                splitURI.remove(segment)
        if len(splitURI) == 2:
            self.bucket, self.key = splitURI
        elif len(splitURI) == 1:
            self.bucket = splitURI[0]
        
        #Get Authenticated User
        self.user = getUser(req)
        
        #Check date
        #check customDateHeader then date header
        
    def write(self, msg):
        self.req.write(msg)