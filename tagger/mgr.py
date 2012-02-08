import tagger.config
import MySQLdb

class Mgr:
	def __init__(self):
		pass
	def showconfig(self):
		tagger.config.show()
	def testconnect(self):
		conn=MySQLdb.connect(
			db=tagger.config.ns_db.p_db,
			host=tagger.config.ns_db.p_host,
			port=tagger.config.ns_db.p_port,
			user=tagger.config.ns_db.p_user,
			passwd=tagger.config.ns_db.p_password,
		)
		conn.close()
		print "connection is ok"
