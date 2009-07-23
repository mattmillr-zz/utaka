'''
Created on Jul 21, 2009

@author: Andrew
'''


from mod_python import apache
from Utaka.src.rest.UtakaRequest import UtakaRequest
#message handler

def handler(req):

    utakaRequest = UtakaRequest(req)

    if utakaRequest.key:
        from Utaka.src.rest.UtakaObject import UtakaObject
        restResource = UtakaObject(utakaRequest)
    elif utakaRequest.bucket:
        from Utaka.src.rest.UtakaBucket import UtakaBucket
        restResource = UtakaBucket(utakaRequest)
    else:
        from Utaka.src.rest.UtakaService import UtakaService
        restResource = UtakaService(utakaRequest)

    return restResource.handleRequest()