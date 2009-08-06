'''
import MySQLdb

connA = MySQLdb.connect('localhost', 'root', 'aburke', 'utaka')
cursorA = connA.cursor()

cursorA.execute("insert into user(username, accesskey, secretkey) values('a', 'a', 'a'),('b', 'b', 'b')")

connA.rollback()

cursorA.execute("insert into user(username, accesskey, secretkey) values('c', 'c', 'c'),('d', 'd', 'd')")

connA.commit()

cursorA.execute("insert into user(username, accesskey, secretkey) values('e', 'e', 'e'),('f', 'f', 'f')")

connA.rollback()

cursorA.execute("select * from user")
res = cursorA.fetchall()
for row in res:
	print str(row)

cursorA.close()
connA.close()
'''

from utaka.src.dataAccess.SingleConnection import Connection as SingleConnection
import MySQLdb
import datetime


dcp = [SingleConnection(True)]
rcp = [SingleConnection(False)]
#timer = datetime.datetime.today()

class Connection:
	def __init__(self, useDictCursor = False):
		try:
			if useDictCursor:
				self.innerConn = dcp.pop()
			else:
				self.innerConn = rcp.pop()
			try:
				self.innerConn.ping()
			except:
				pass
			utakaLog = open('/var/www/html/utaka/utakaLog', 'a')
			try:
				if self.usingDictCursor():
					utakaLog.write('Dictionary Database Connection Pulled from Pool\r\n')
				else:
					utakaLog.write('Regular Database Connection Pulled from Pool\r\n')
			finally:
				utakaLog.close()
		except IndexError:
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
