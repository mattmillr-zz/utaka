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

'''
Created Aug 4, 2009

connection pool abstraction over previous Connection.py which is now SingleConnection.py
sets up module scope connection pool, currently with no size limit
	pool for both connections with dictionary cursors and regular cursors
reconnects to db every x hours depending on config file
@author: Andrew
'''

from utaka.src.dataAccess.SingleConnection import Connection as SingleConnection
import utaka.src.Config as Config
import MySQLdb
import datetime

dcp = [SingleConnection(True)]
rcp = [SingleConnection(False)]
dbTimer = datetime.datetime.today()
dbTimeout = datetime.timedelta(hours = int(Config.get('database', 'connection_timeout_in_hours')))

class Connection:
	def __init__(self, useDictCursor = False):
		if len(dcp) > 0:
			if useDictCursor:
				self.innerConn = dcp.pop()
			else:
				self.innerConn = rcp.pop()
			now = datetime.datetime.today()
			if (now - dbTimeout) > self.innerConn.connectTime:
				self.innerConn.close()
				self.innerConn = SingleConnection(useDictCursor)
		else:
			self.innerConn = SingleConnection(useDictCursor)

	def usingDictCursor(self):
		return self.innerConn.usingDictCursor()

	def executeStatement(self, statement, placeholder):
		return self.innerConn.executeStatement(statement, placeholder)

	def getRowCount(self):
		return self.innerConn.rowcount()

	def commit(self):
		self.innerConn.commit()
		
	def rollback(self):
		self.innerConn.rollback()
		
	def close(self):
		self.commit()
		self.__close_()
	
	def cancelAndClose(self):
		self.rollback()
		self.__close_()

	def __close_(self):
		utakaLog = open('/var/www/html/utaka/utakaLog', 'a')
		try:
			if self.usingDictCursor():
				utakaLog.write('Dictionary Database Connection Returned to Pool\r\n')
			else:
				utakaLog.write('Regular Database Connection Returned to Pool\r\n')
		finally:
			utakaLog.close()
		if self.usingDictCursor():
			dcp.append(self.innerConn)
		else:
			rcp.append(self.innerConn)
		self.innerConn = None
