import tagger.config
import MySQLdb

class Mgr:
	def __init__(self):
		pass
	""" helpers """
	def connect(self):
		self.conn=MySQLdb.connect(
			db=tagger.config.ns_db.p_db,
			host=tagger.config.ns_db.p_host,
			port=tagger.config.ns_db.p_port,
			user=tagger.config.ns_db.p_user,
			passwd=tagger.config.ns_db.p_password,
		)
	def disconnect(self):
		self.conn.close()
	""" ops that can be launched from the command line """
	def showconfig(self):
		tagger.config.show()
	def testconnect(self):
		self.connect()
		self.disconnect()
		print "connection is ok"
	def create(self):
		print "creating..."
