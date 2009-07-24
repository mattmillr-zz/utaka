from utaka.src.errors.UtakaErrors import UtakaError

class BucketWriteError(UtakaError):
    def __init__(self, msg):
        msg = "BucketWriteError: " + msg
        UtakaError.__init__(self, msg)