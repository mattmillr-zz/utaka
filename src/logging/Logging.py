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
Created August 6, 2009

Logging
@author: Andrew
'''
import logging
import utaka.src.Config as Config
import datetime

LOG_FILEPATH = Config.get('logging', 'path')
LOG_LEVEL = logging.DEBUG
BUCKET_LOG_LEVEL = logging.DEBUG
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

def logDebug(msg):
	__logging_(msg, logging.DEBUG)
def logInfo(msg):
	__logging_(msg, logging.INFO)
def logWarn(msg):
	__logging_(msg, logging.WARN)
def logError(msg):
	__logging_(msg, logging.ERROR)
def logCritical(msg):
	__logging_(msg, logging.CRITICAL)
def __logging_(msg, lvl):
	fp = LOG_FILEPATH + str(datetime.date.today())
	logging.basicConfig(filename = fp, level = LOG_LEVEL, format = LOG_FORMAT)
	logging.log(lvl, msg)
	logging.shutdown()

def bucketLogDebug(bucket, msg):
	__bucketLogging_(bucket, msg, logging.DEBUG)
def bucketLogInfo(bucket, msg):
	__bucketLogging_(bucket, msg, logging.INFO)
def bucketLogWarn(bucket, msg):
	__bucketLogging_(bucket, msg, logging.WARN)
def bucketLogError(bucket, msg):
	__bucketLogging_(bucket, msg, logging.ERROR)
def bucketLogCritical(bucket, msg):
	__bucketLogging_(bucket, msg, logging.CRITICAL)
def __bucketLogging_(bucket, msg, lvl):
	fp = LOG_FILEPATH + bucket + ':' + str(datetime.date.today())
	logging.basicConfig(filename = fp, level = BUCKET_LOG_LEVEL, format = LOG_FORMAT)
	logging.log(lvl, msg)
	logging.shutdown()