
import utaka.src.core.Bucket as Bucket
import utaka.src.accessControl.BucketACP as BucketACP
import utaka.src.logging.Bucket as BucketLogging


def getBucket(user, bucket, prefix, marker, maxKeys, delimiter):
	if not BucketACP.checkUserPermission(user, bucket, 'read'):
		raise Exception, 'forbidden action'
		'''not allowed, throw error'''
	BucketLogging.logEvent(bucket, user, 'read_bucket')
	return Bucket.getBucket(userId=user, bucket=bucket, prefix=prefix, marker=marker, maxKeys=maxKeys, delimiter=delimiter)


def setBucket(user, bucket, accessControlPolicy):
	if not user:
		raise Exception, 'forbidden action'
	BucketLogging.logEvent(bucket, user, 'write_bucket')
	Bucket.setBucket(userId = user, bucket = bucket)
	BucketLogging.logEvent(bucket, user, 'write_acp')
	BucketACP.setBucketACP(bucket, accessControlPolicy)

def destroyBucket(user, bucket):
	if not BucketACP.checkUserPermission(user, bucket, 'destroy'):
		raise Exception, 'forbidden action'


def getBucketACP(user, bucket):
	if not BucketACP.checkUserPermission( user, bucket, 'read_acp'):
		raise Exception, 'forbidden action'
	BucketLogging.logEvent(bucket, user, 'read_bucket_acp')
	return BucketACP.getBucketACP(bucket)


def setBucketACP(user, bucket, accessControlPolicy):
	if not BucketACP.checkUserPermission(user, bucket, 'write_acp'):
		raise Exception, 'forbidden action'
	BucketLogging.logEvent(bucket, user, 'write_bucket_acp')
	BucketACP.setBucketACP(bucket, accessControlPolicy)


def setBucketLogStatus(user, srcBucket, logBucket):
	if not BucketACP.checkUserPermission(user, bucket, 'write_log_status'):
		raise Exception, 'forbidden action'
	BucketLogging.logEvent(bucket, user, 'write_log_status')
	return BucketLogging.setBucketLogStatus(srcBucket, logBucket)


def getBucketLogStatus(user, bucket):
	if not BucketACP.checkUserPermission(user, bucket, 'read_log_status'):
		raise Exception, 'forbidden action'
	BucketLogging.logEvent(bucket, user, 'read_log_status')
	return BucketLogging.getBucketLogStatus(bucket)