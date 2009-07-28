
import utaka.src.core.Bucket as Bucket
import utaka.src.accessControl.BucketACP as BucketACP


def getBucket(userId, bucket, prefix, marker, maxKeys, delimiter):
	if not checkUserPermission(user, bucket, 'read'):
		'''not allowed, throw error'''
	return Bucket.getBucket(bucket, prefix, marker, maxKeys, delimiter)
	
def setBucket(userId, bucket, accessControlList):
	if not checkUserPermission(user, bucket, 'write'):
		'''not allowed, throw error'''
	Bucket.setBucket(userId, bucket)
	if accessControlList:
		BucketACP.setBucketACP(bucket, accessControlList)