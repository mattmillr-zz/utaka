'''
Created on Jul 21, 2009

@author: Andrew
'''


from mod_python import apache
from Utaka.UtakaRequest import UtakaRequest
#message handler

def handler(req):

    utakaRequest = UtakaRequest(req)

    if utakaRequest.key:
        from Utaka.RestResources.UtakaObject import UtakaObject
        restResource = UtakaObject(utakaRequest)
    elif utakaRequest.bucket:
        from Utaka.RestResources.UtakaBucket import UtakaBucket
        restResource = UtakaBucket(utakaRequest)
    else:
        from Utaka.RestResources.UtakaService import UtakaService
        restResource = UtakaService(utakaRequest)

    return restResource.handleRequest()