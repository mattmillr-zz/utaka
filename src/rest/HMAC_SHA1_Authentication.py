'''
Created on Jul 21, 2009

@author: Andrew
'''




from mod_python import apache
from mod_python import util
from Utaka.Exceptions.ServerExceptions import ServerException
import Utaka.config as config

def getUser(req):

    __user = None
    try:
        __header = config.get('authentication', 'header')
        __prefix = config.get('authentication', 'prefix') + " "
    except ServerException, e:
        raise apache.SERVER_RETURN, apache.HTTP_INTERNAL_SERVER_ERROR
    else:
        try:
            __authString = req.headers_in[__header]
        except KeyError:
            pass
        else:
            __splitAuth = __authString.split(__prefix)
            if len(__splitAuth) == 2 and len(__splitAuth[0]) == 0:
                try:
                    __accessKey, __signature = __splitAuth[1].split(':')
                except ValueError, e:
                    raise apache.SERVER_RETURN, apache.HTTP_BAD_REQUEST
                else:
                    try:
                        #establish connection and query for user and key
                        __host = config.get('authentication', 'mysql_hostname')
                        __user = config.get('authentication', 'mysql_username')
                        __upw = config.get('authentication', 'mysql_password')
                        __db = config.get('authentication', 'mysql_database')
                        from Utaka.DataAccess import connection
                        __conn = connection.Connection(__host, __user, __upw, __db)
                        __dbResult = __conn.executeStatement('select userid, secretKey from user where accessKey = %s', (__accessKey,))
                        __user, __secretKey = __dbResult[0]
                    except Exception:
                        raise apache.SERVER_RETURN, apache.HTTP_INTERNAL_SERVER_ERROR
                    else:
                        #compute sig and compare
                        __computedSig = __computeBase64Signature(__secretKey, __buildStringToSign(req))
                        if __computedSig != __signature:
                            raise apache.SERVER_RETURN, apache.HTTP_FORBIDDEN
        return __user


def __buildStringToSign(req):
    nl = '\n'
    
    #http headers
    methodString = req.method
    contentMd5String = req.headers_in.get('content-md5', '')
    contentTypeString = req.headers_in.get('content-type', '')
    dateString = req.headers_in.get('date', '')
        
    #Canonicalize Custom Headers
    __customHeaderPrefix = config.get('common', 'customHeaderPrefix').lower()
    __customDateHeader = __customHeaderPrefix + "-date"
    
    canCustomHeaders = ''
    customHeaderList = []
    
    for val in req.headers_in.keys():
        if val.lower().startswith(__customHeaderPrefix):
            customHeaderList.insert(val.lower() + ':' + req.headers_in[val].lstrip() + nl)
            if val.lower() == __customDateHeader:
                dateString = ''
                
    customHeaderList.sort()
    for val in customHeaderList:
        canCustomHeaders += val
    
    
    #Canoicalize URI
    uriString = req.uri
    if req.args:
        req.write('ARGS FOUND\n')
        if req.args.find('acl') > -1:
            req.write('ACL ARG FOUND\n')
            uriString += '?acl?log'
    return (methodString + nl + contentMd5String + nl + 
            contentTypeString + nl + dateString + nl + canCustomHeaders + uriString)
    
def __computeBase64Signature(key, message, urlEncode=False):
    import base64
    import hmac
    import sha
    b64Str = base64.encodestring(hmac.new(key, message, sha).digest()).strip()
    if urlEncode:
        import urllib
        b64Str = urllib.quote_plus(b64Str)
    return b64Str