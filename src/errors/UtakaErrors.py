'''
Created on Jul 10, 2009

@author: Andrew
'''

class UtakaError(Exception):
    def __init__(self, msg):
        self.message = msg
    def __str__(self):
        return self.message