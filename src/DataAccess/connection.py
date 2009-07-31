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
import utaka.src.config as config
import utaka.src.exceptions.InternalErrorException as InternalErrorException

class Connection:

	def __init__(self, connectionType = "utaka", useDictCursor = False):
		host = config.get('database','mysql_utaka_hostname')
		user = config.get('database','mysql_utaka_username')
		passwd = config.get('database','mysql_utaka_password')
		db = config.get('database','mysql_utaka_database')
		try:
			self.__conn = MySQLdb.connect(host = host, user = user, passwd = passwd, db = db)
			if useDictCursor:
				self.__usingDictCursor = True
				self.__cursor = self.__conn.cursor(MySQLdb.cursors.DictCursor)
			else:
				self.__usingDictCursor = False
				self.__cursor = self.__conn.cursor()
		except MySQLdb.DatabaseError, e:
			raise InternalErrorException.DatabaseErrorException(e)

	def usingDictCursor(self):
			return self.__usingDictCursor
			
	def executeStatement(self, statement, placeholder):
		try:
			self.__cursor.execute(statement, placeholder)
			return self.__cursor.fetchall()
		except MySQLdb.DatabaseError, e:
			raise InternalErrorException.DatabaseErrorException(e)
			
	def close(self):
		try:
			self.__cursor.close()
			self.__conn.commit()
			self.__conn.close()
		except MySQLdb.DatabaseError, e:
			raise InternalErrorException.DatabaseErrorException(e)
			
	def cancelAndClose(self):
		try:
			self.__cursor.close()
			self.__conn.close()
		except MySQLdb.DatabaseError, e:
			raise InternalErrorException.DatabaseErrorException(e)