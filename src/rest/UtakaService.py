'''
Created on Jul 21, 2009

@author: Andrew
'''




class UtakaService:

    def __init__(self, utakaReq):
        self.req = utakaReq
        
    def handleRequest(self):
        if self.req.method == 'GET':
            '''GET'''
            
            
    def __checkUserPermission(self):
        '''throw forbidden error'''