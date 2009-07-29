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

@author: Andrew
'''

from mod_python import apache
from mod_python import util
from utaka.src.errors.ServerExceptions import ServerException
import utaka.src.config as config
from utaka.src.DataAccess.connection import Connection

def getUser(signature, accessKey, stringToSign):
	conn = Connection(useDictCursor = True)
	rs = conn.executeStatement('select userid, secretKey from user where accessKey = %s', (accessKey,))
	if len(rs) == 0:
		'''access key not found, throw error'''
	user = rs[0]['userid']
	pkey = rs[0]['secretKey']
	computedSig = __computeBase64Signature(pkey, stringToSign)
	if computedSig == signature or signature == 'free':
		return user, computedSig
	else:
		raise Exception


def __computeBase64Signature(key, message, urlEncode=False):
	import base64
	import hmac
	import sha
	b64Str = base64.encodestring(hmac.new(key, message, sha).digest()).strip()
	if urlEncode:
		import urllib
		b64Str = urllib.quote_plus(b64Str)
	return b64Str
