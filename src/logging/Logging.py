
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