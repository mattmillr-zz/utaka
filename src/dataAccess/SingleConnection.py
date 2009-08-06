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

import MySQLdb
import utaka.src.Config as Config
import utaka.src.exceptions.InternalErrorException as InternalErrorException

class Connection:

	def __init__(self, useDictCursor = False):
		host = Config.get('database','mysql_utaka_hostname')
		user = Config.get('database','mysql_utaka_username')
		passwd = Config.get('database','mysql_utaka_password')
		db = Config.get('database','mysql_utaka_database')
		self.conn = MySQLdb.connect(host = host, user = user, passwd = passwd, db = db)
		if useDictCursor:
			self._usingDictCursor = True
			self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
		else:
			self._usingDictCursor = False
			self.cursor = self.conn.cursor()
		utakaLog = open('/var/www/html/utaka/utakaLog', 'a')
		try:
			if self._usingDictCursor:
				utakaLog.write('Dictionary Database Connection Made\r\n')
			else:
				utakaLog.write('Regular Database Connection Made\r\n')
		finally:
			utakaLog.close()

	def usingDictCursor(self):
			return self._usingDictCursor

	def executeStatement(self, statement, placeholder):
		try:
			self.cursor.execute(statement, placeholder)
		except MySQLdb.IntegrityError, e:
			raise InternalErrorException.DatabaseIntegrityErrorException(e)
		return self.cursor.fetchall()

	def getRowCount(self):
		'''returns cursor.rowcount()'''
		return self.cursor.rowcount
		
	def ping(self):
		self.conn.ping()

	def commit(self):
		self.conn.commit()
		
	def rollback(self):
		self.conn.rollback()
		
	def close(self):
		self.cursor.close()
		self.conn.commit()
		self.conn.close()

	def cancelAndClose(self):
		self.cursor.close()
		self.conn.close()