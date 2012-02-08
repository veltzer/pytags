import tagger.config
import MySQLdb
import warnings

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
		# remove mysql warnings...
		if tagger.config.ns_mgr.p_suppress_warnings:
			warnings.filterwarnings('ignore', category = MySQLdb.Warning)
	def disconnect(self):
		self.conn.close()
	def execute(self,stmt):
		"""
		Run the given query, commit changes
		"""
		cursor=self.conn.cursor()
		num_affected_rows=cursor.execute(stmt)
		cursor.close()
		self.conn.commit()
		return num_affected_rows
	""" ops that can be launched from the command line """
	def showconfig(self):
		tagger.config.show()
	def testconnect(self):
		self.connect()
		self.disconnect()
		#print "connection is ok"
	def create(self):
		self.connect()
		if tagger.config.ns_op.p_force:
			self.execute('DROP TABLE IF EXISTS TbTag');
		self.execute("""
			CREATE TABLE TbTag (
				id INT NOT NULL AUTO_INCREMENT,
				name VARCHAR(40) NOT NULL,
				PRIMARY KEY(id),
				UNIQUE KEY name (name)
			) ENGINE=InnoDB
		""")
		self.disconnect()
