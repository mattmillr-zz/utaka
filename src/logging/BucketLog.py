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
Created on Aug 6, 2009
event interface over bucket logging
@author Andrew
'''
import utaka.src.dataAccess.Connection as Connection
import utaka.src.Config as Config
import utaka.src.logging.Logging as Logging
import utaka.src.exceptions.InternalErrorException as InternalErrorException

def setBucketLogStatus(srcBucket, logBucket):
	pass

def getBucketLogStatus(bucket):
	pass

def logBucketEvent(user, bucket, action):
	if not user:
		user = 'ANNON'
	if action not in ('get', 'set', 'get_acp', 'set_acp', 'get_log_status', 'set_log_status', 'delete'):
		raise InternalErrorException.BadArgumentException('action', str(action), 'permitted actions for logging bucket events are [get, set, get_acp, set_acp, get_log_status, set_log_status, delete]')
	Logging.bucketLogInfo(bucket, 'bucket_%s,user=%s' % (action, str(user)))

def logKeyEvent(user, bucket, key, action, keyDigest=None):
	if not user:
		user = 'ANNON'
	if not keyDigest:
		keyDigest = 'NOTPROVIDED'
	if action in ('get', 'get_acp', 'set_acp', 'delete'):
		Logging.bucketLogInfo(bucket, 'object_%s,user=%s,key=%s' % (action, str(user), key))
	elif action == 'set':
		Logging.bucketLogInfo(bucket, 'object_set,user=%s,key=%s,keyDigest=%s' % (str(user), key, keyDigest))
	else:
		raise InternalErrorException.BadArgumentException('action', str(action), 'permitted actions for logging key events are [get, set, get_acp, set_acp, delete]')