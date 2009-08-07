

import utaka.src.core.Bucket as Bucket
import utaka.src.accessControl.BucketACP as BucketACP
import utaka.src.logging.BucketLog as BucketLogging
import utaka.src.exceptions.ForbiddenException as ForbiddenException
import utaka.src.exceptions.ConflictException as ConflictException


def getBucket(user, bucket, prefix, marker, maxKeys, delimiter):
	if not BucketACP.checkUserPermission(user, bucket, 'read'):
		raise ForbiddenException.AccessDeniedException()
	BucketLogging.logBucketEvent(user, bucket, 'get')
	return Bucket.getBucket(bucket=bucket, prefix=prefix, marker=marker, maxKeys=maxKeys, delimiter=delimiter)


def setBucket(user, bucket, accessControlPolicy):
	if not user:
		raise ForbiddenException.AccessDeniedException()
	try:
		Bucket.setBucket(userid = user, bucket = bucket)
	except ConflictException.BucketAlreadyOwnedByYouException:
		pass
	BucketLogging.logBucketEvent(user, bucket, 'set')
	BucketACP.setBucketACP(bucket, accessControlPolicy)
	BucketLogging.logBucketEvent(user, bucket, 'set_acp')


def destroyBucket(user, bucket):
	if not BucketACP.checkUserPermission(user, bucket, 'destroy'):
		raise ForbiddenException.AccessDeniedException()
	Bucket.destroyBucket(bucket)
	BucketLogging.logBucketEvent(user, bucket, 'delete')


def getBucketACP(user, bucket):
	if not BucketACP.checkUserPermission( user, bucket, 'read_acp'):
		raise ForbiddenException.AccessDeniedException()
	BucketLogging.logBucketEvent(user, bucket, 'get_acp')
	return BucketACP.getBucketACP(bucket)


def setBucketACP(user, bucket, accessControlPolicy):
	if not BucketACP.checkUserPermission(user, bucket, 'write_acp'):
		raise ForbiddenException.AccessDeniedException()
	BucketACP.setBucketACP(bucket, accessControlPolicy)
	BucketLogging.logBucketEvent(user, bucket, 'set_acp')


def setBucketLogStatus(user, srcBucket, logBucket):
	if not BucketACP.checkUserPermission(user, bucket, 'write_log_status'):
		raise ForbiddenException.AccessDeniedException()
	if not BucketACP.checkUserPermission(user, bucket, 'write'):
		raise ForbiddenException.AccessDeniedException()
	BucketLogging.logBucketEvent(user, bucket, 'set_log_status')
	return BucketLogging.setBucketLogStatus(srcBucket, logBucket)


def getBucketLogStatus(user, bucket):
	if not BucketACP.checkUserPermission(user, bucket, 'read_log_status'):
		raise ForbiddenException.AccessDeniedException()
	BucketLogging.logBucketEvent(user, bucket, 'get_log_status')
	return BucketLogging.getBucketLogStatus(bucket)