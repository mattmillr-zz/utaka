
import utaka.src.core.Object as Object
import utaka.src.accessControl.ObjectACP as ObjectACP
import utaka.src.accessControl.BucketACP as BucketACP
import utaka.src.logging.Bucket as BucketLogging

def getObject(user, bucket, key, getMetadata, getData, byteRangeStart, byteRangeEnd, ifMatch, ifNotMatch, ifModifiedSince, ifNotModifiedSince, ifRange):
	if not ObjectACP.checkUserPermission(user, bucket, key, 'read'):
		raise Exception, 'forbidden action'
	BucketLogging.logEvent(bucket, key, user, 'read')
	return Object.getObject(userId = user, bucket = bucket, key=key, getMetadata=getMetadata, getData=getData, byteRangeStart=byteRangeStart, byteRangeEnd=byteRangeEnd, ifMatch=ifMatch, ifNotMatch=ifNotMatch, ifModifiedSince=ifModifiedSince, ifNotModifiedSince=ifNotModifiedSince, ifRange=ifRange)



def setObject(user, bucket, key, metadata, data, contentMd5, contentType, contentDisposition, contentEncoding, accessControlPolicy):
	if not BucketACP.checkUserPermission(user, bucket, 'write'):
		raise Exception, 'forbidden action'
	BucketLogging.logEvent(bucket, key, user, 'write')
	result = Object.setObject(userId = user, bucket=bucket, key=key, metadata=metadata, data=data, content_md5 = contentMd5, content_type=contentType, content_disposition=contentDisposition, content_encoding=contentEncoding)
	ObjectACP.setObjectACP(bucket, key, accessControlPolicy)
	
def cloneObject(user, sourceBucket, sourceKey, destinationBucket, destinationKey, metadata, ifMatch, ifNotMatch, ifModifiedSince, ifNotModifiedSince):
	pass
	
def deleteObject(user, bucket, key):
	pass
	
def setObjectACP(user, bucket, key, accessControlPolicy):
	if not ObjectACP.checkUserPermission(user, bucket, key, 'write_acp'):
		raise Exception, 'forbidden action'
	BucketLogging.logEvent(bucket, key, user, 'write_acp')
	ObjectACP.setObjectACP(bucket, key, accessControlPolicy)
	
def getObjectACP(user, bucket, key):
	if not ObjectACP.checkUserPermission(user, bucket, key, 'read_acp'):
		raise Exception, 'forbidden action'
	BucketLogging.logEvent(bucket, key, user, 'read_acp')
	return ObjectACP.getObjectACP(bucket, key)
