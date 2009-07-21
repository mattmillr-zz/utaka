'''
Created on Jul 21, 2009

@author: Andrew
'''




from mod_python import apache

class UtakaBucket:

    def __init__(self, utakaReq):
        self.req = utakaReq
        
        
        
    def handleRequest(self):

        if self.req.srACL:
            if self.req.method == 'GET':
                '''GET ACL'''
            elif self.req.method == 'PUT':
                '''PUT ACL'''

        elif self.req.srLogging:
            if self.req.method == 'GET':
                '''GET LOGGING'''
            elif self.req.method == 'PUT':
                '''PUT LOGGING'''

        elif self.req.srLocation:
            if self.req.method == 'GET':
                '''GET LOCATION'''
            elif self.req.method == 'PUT':
                '''PUT LOCATION'''

        else:
            if self.req.method == 'GET':
                '''GET'''
            elif self.req.method == 'PUT':
                '''PUT'''
            elif self.req.method == 'POST':
                '''POST'''
            elif self.req.method == 'COPY':
                '''COPY'''
            elif self.req.method == 'DELETE':
                '''DELETE'''
                
        return apache.OK