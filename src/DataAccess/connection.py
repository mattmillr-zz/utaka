'''
Created on Jul 21, 2009

@author: Andrew
'''
import MySQLdb

class Connection:

    def __init__(self, host, user, passwd, db, useDictCursor = False):
        self.__conn = MySQLdb.connect(host = host, user = user, passwd = passwd, db = db)
        if useDictCursor:
            self.__usingDictCursor = True
            self.__cursor = self.__conn.cursor(MySQLdb.cursors.DictCursor)
        else:
            self.__usingDictCursor = False
            self.__cursor = self.__conn.cursor()
        
    def usingDictCursor(self):
        return self.__usingDictCursor
        
    def executeStatement(self, statement, placeholder):
        self.__cursor.execute(statement, placeholder)
        return self.__cursor.fetchall()
        
    def close(self):
        self.__cursor.close()
        self.__conn.commit()
        self.__conn.close()
        
    def cancelAndClose(self):
        self.__cursor.close()
        self.__conn.close()