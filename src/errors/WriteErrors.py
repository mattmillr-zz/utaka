from utaka.src.errors.UtakaErrors import UtakaError

class BucketWriteError(UtakaError):
    def __init__(self, msg):
        msg = "BucketWriteError: " + msg
        UtakaError.__init__(self, msg)

class ObjectWriteError(UtakaError):
    def __init__(self, msg):
        msg = "ObjectWriteError: " + msg
        UtakaError.__init__(self, msg)

class UserWriteError(UtakaError):
    def __init__(self, msg):
        msg = "UserWriteError: " + msg
        UtakaError.__init__(self, msg)