'''
Created on Jul 22, 2009

@author: Andrew
'''

import ConfigParser
from Utaka.Exceptions.ServerExceptions import ServerException

configFile = "/var/www/html/Utaka/.utaka_config"

config = ConfigParser.ConfigParser()

config.read(configFile)

def get (section, key):
    try:
        return config.get(section, key)
    except:
        raise ServerException('configuration problem')