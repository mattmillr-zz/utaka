#Copyright 2009 Humanitarian International Services Group
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.
'''
Created on Jul 21, 2009
For authentication of utaka users using keyed-hash message
@author: Andrew
'''

from utaka.src.dataAccess.Connection import Connection
import utaka.src.exceptions.ForbiddenException as ForbiddenException
import utaka.src.config as Config

'''
getUser
	params:
		signature - passed in signature
		accessKey - key to authenticate stringToSign with
		stringToSign - string to be authenticated
	returns:
		user - userid
		isAdmin - bool...whether or not user has admin capabilities
		computedSig - the computed signature
	local raises:
		InvalidAccessKeyIdException - accesskeyid was not found in system
		SignatureDoesNotMatchException
		
'''
def getUser(signature, accessKey, stringToSign):
	conn = Connection(useDictCursor = True)
	try:
		rs = conn.executeStatement('select userid, secretKey, isAdmin from user where accessKey = %s', (accessKey,))
	finally:
		conn.close()
	if len(rs) == 0:
		raise ForbiddenException.InvalidAccessKeyIdException(accessKey)
	user = rs[0]['userid']
	pkey = rs[0]['secretKey']
	isAdmin = rs[0]['isAdmin']
	computedSig = __computeBase64Signature(pkey, stringToSign)
	mode = Config.get('common', 'mode')
	if computedSig == signature or (mode == 'debug' and signature == 'free'):
		return user, isAdmin, computedSig
	else:
		stringToSignByteSeq = []
		for c in stringToSign:
			stringToSignByteSeq.append(c.encode('hex'))
		raise ForbiddenException.SignatureDoesNotMatchException(' '.join(stringToSignByteSeq), stringToSign, signature, accessKey)


def __computeBase64Signature(key, message, urlEncode=False):
	import base64
	import hmac
	import sha
	b64Str = base64.encodestring(hmac.new(key, message, sha).digest()).strip()
	if urlEncode:
		import urllib
		b64Str = urllib.quote_plus(b64Str)
	return b64Str