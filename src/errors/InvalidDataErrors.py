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

from utaka.src.errors.UtakaErrors import UtakaError

class UtakaInvalidDataError(UtakaError):
    def __init__(self, msg):
        msg = "UtakaDataFormatError: " + msg
        UtakaError.__init__(self, msg)
        
class UtakaInvalidUserError(UtakaInvalidDataError):
    def __init__(self, msg):
        msg = "InvalidUser: " + msg
        UtakaInvalidDataError.__init__(self, msg)
        
class UtakaInvalidBucketError(UtakaInvalidDataError):
    def __init__(self, msg):
        msg = "InvalidBucket: " + msg
        UtakaInvalidDataError.__init__(self, msg)
        
class UtakaInvalidKeyError(UtakaInvalidDataError):
    def __init__(self, msg):
        msg = "InvalidKey: " + msg
        UtakaInvalidDataError.__init__(self, msg)
        
class UtakaInvalidArgumentError(UtakaInvalidDataError):
    def __init__(self, msg):
        msg = "InvalidArgument: " + msg
        UtakaInvalidDataError.__init__(self, msg)

class UtakaInvalidConfigurationError(UtakaInvalidDataError):
    def __init__(self, msg):
        msg = "InvalidConfiguration: " + msg
        UtakaInvalidDataError.__init__(self, msg)