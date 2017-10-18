import os
from urllib import parse
import psycopg2
import psycopg2.extras

class SQLServices():
	dbconn=None
	dbcur=None
	def Connect(self):
		try:
			self.dbconn = psycopg2.connect(
    			database="dfctn7g5et59he",
    			user="xknobmcpqbhtcv",
    			password="36eda7a8ae0c7240c202cc8b264e5046114f136c85b20652907a1db5228ebd73",
    			host="ec2-79-125-125-97.eu-west-1.compute.amazonaws.com",
    			port="5432"
			)
			self.dbcur=self.dbconn.cursor(cursor_factory=psycopg2.extras.DictCursor)
			return True
		except:
			return False
	def Disconnect(self):
		if self.dbcur:
			self.dbcur.close()
			self.dbcur=None
		if self.dbconn:
			self.dbconn.close()
			self.dbconn=None
	def AddMemo(self,UserID,String):
		if not self.dbcur:
			return False
		if not self.dbconn:
			return False
		try:
			self.dbcur.execute('INSERT INTO memorandum("String", "UserID")VALUES (%s, %s);',(String,UserID,))
			self.dbconn.commit()
			return True
		except:
			self.dbconn.rollback()
			return False
	def DelMemo(self,UserID,ID):
		if not self.dbcur:
			return False
		if not self.dbconn:
			return False
		try:
			self.dbcur.execute('DELETE FROM memorandum WHERE ("ID"=%s AND "UserID"=%s);',(ID,UserID,))
			self.dbconn.commit()
			return True
		except:
			self.dbconn.rollback()
			return False
	def UpdMemo(self,ID,UserID,String):
		if not self.dbcur:
			return False
		if not self.dbconn:
			return False
		try:
			self.dbcur.execute('UPDATE memorandum SET "String"=%s WHERE ("ID"=%s and "UserID"=%s);',(String,ID,UserID,))
			self.dbconn.commit()
			return True
		except:
			self.dbconn.rollback()
			return False
	def ListMemo(self,UserID):
		resList=[]
		try:
			self.dbcur.execute('SELECT "ID", "String" FROM memorandum WHERE ("UserID"=%s);',(UserID,))
			res=self.dbcur.fetchall()
			for rec in res:
				line=str(rec['ID'])+'||'+str(rec['String'])
				resList.append(line)
			return resList
		except:
			resList.clear()
			resList.append("SQL Query executes Fail!")
			return resList
	def AddRes(self,Name,Link):
		if not self.dbcur:
			return False
		if not self.dbconn:
			return False
		try:
			self.dbcur.execute('INSERT INTO resource("Name", "Link")VALUES (%s, %s);',(Name,Link,))
			self.dbconn.commit()
			return True
		except:
			self.dbconn.rollback()
			return False
	def DelRes(self,ID):
		if not self.dbcur:
			return False
		if not self.dbconn:
			return False
		try:
			self.dbcur.execute('DELETE FROM resource WHERE ("ID"=%s);',(ID,))
			self.dbconn.commit()
			return True
		except:
			self.dbconn.rollback()
			return False

	def ListRes(self):
		resList=[]
		try:
			self.dbcur.execute('SELECT "ID", "Name", "Link", "Stamp" FROM resource;')
			res=self.dbcur.fetchall()
			for rec in res:
				line=str(rec['ID'])+'||'+str(rec['Name'])+'||'+str(rec['Link'])
				resList.append(line)
			return resList
		except:
			resList.clear()
			resList.append("SQL Query executes Fail!")
			return resList
	def CleanUp(self):
		if not self.dbcur:
			return False
		if not self.dbconn:
			return False
		self.dbcur.execute('select "ID" from memorandum WHERE "Stamp"+interval \'45 day\'<now()')
		res1=self.dbcur.fetchall()
		self.dbcur.execute('select "ID" from resource WHERE "Stamp"+interval \'45 day\'<now()')
		res2=self.dbcur.fetchall()
		try:
			for rec in res1:
				#dosomthing
				tar=str(rec['ID'])
				self.dbcur.execute('DELETE FROM memorandum WHERE ("ID"=%s)',(tar,))
			print("Start cleanup resource")
			for rec in res2:
				#dosomthing
				tar=str(rec['ID'])
				self.dbcur.execute('DELETE FROM resource WHERE ("ID"=%s)',(tar,))
			self.dbconn.commit()
			return True
		except:
			self.dbconn.rollback()
			return False
	def Usage(self):
		if not self.dbcur:
			return -1
		if not self.dbconn:
			return -1
		try:
			self.dbcur.execute('SELECT count(*) as Num FROM memorandum;')
			res1=self.dbcur.fetchone()
			num=int(res1[0])
			self.dbcur.execute('SELECT count(*) as Num FROM resource;')
			res2=self.dbcur.fetchone()
			num+=int(res2[0])
			return num
		except:
			return -1