'''
Created on Jul 21, 2009

@author: Andrew
'''




class UtakaObject:
    
    def __init__(self, utakaReq):
        self.req = utakaReq


    def handleRequest(self):

        if self.req.srACL:
            if self.req.method == 'GET':
                '''GET ACL'''
            elif self.req.method == 'PUT':
                '''PUT ACL'''                

        else:
            if self.req.method == 'GET':
                '''GET'''
            elif self.req.method == 'PUT':
                '''PUT'''
            elif self.req.method == 'POST':
                '''POST'''
            elif self.req.method == 'HEAD':
                '''HEAD'''
            elif self.req.method == 'COPY':
                '''COPY'''
            elif self.req.method == 'DELETE':
                '''DELETE'''



    def __checkUserPermission(self):
        '''throw forbidden error'''
        