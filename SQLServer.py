import os
from urllib import parse
import psycopg2
import psycopg2.extras

class SQLServices():
	dbconn=None
	dbcur=None
	def Connect(self):
		try:
			urlparse.uses_netloc.append("postgres")
			url = urlparse.urlparse(os.environ["DATABASE_URL"])

			self.dbconn = psycopg2.connect(
    			database=url.path[1:],
    			user=url.username,
    			password=url.password,
    			host=url.hostname,
    			port=url.port
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
	def DelMemo(self,ID):
		if not self.dbcur:
			return False
		if not self.dbconn:
			return False
	def UpdMemo(self,ID,UserID,String):
		if not self.dbcur:
			return False
		if not self.dbconn:
			return False
	def ListMemo(self,UserID):
		pass
	def AddRes(self,Name,Link):
		if not self.dbcur:
			return False
		if not self.dbconn:
			return False
	def DelRes(self,ID):
		if not self.dbcur:
			return False
		if not self.dbconn:
			return False
	def ListRes(self):
		pass
	def CleanUp(self):
		if not self.dbcur:
			return False
		if not self.dbconn:
			return False
		print("Start cleanup")
		self.dbcur.execute('select "ID" from memorandum WHERE "Stamp"+interval \'45 day\'<now()')
		res1=self.dbcur.fetchall()
		self.dbcur.execute('select "ID" from resource WHERE "Stamp"+interval \'45 day\'<now()')
		res2=self.dbcur.fetchall()
		try:
			for rec in res1:
				#dosomthing
				tar=str(rec['ID'])
				print("from memorandum DEL ID:"+tar)
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
			print("Start count")
			self.dbcur.execute('SELECT count(*) as Num FROM memorandum;')
			res1=self.dbcur.fetchone()
			num=int(res1[0])
			self.dbcur.execute('SELECT count(*) as Num FROM resource;')
			res2=self.dbcur.fetchone()
			num+=int(res2[0])
			return num
		except:
			return -1