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
	def create(self):
		self.connect()
		if tagger.config.ns_op.p_force:
			self.execute('DROP TABLE IF EXISTS TbFileTag');
			self.execute('DROP TABLE IF EXISTS TbFile');
			self.execute('DROP TABLE IF EXISTS TbTagRelations');
			self.execute('DROP TABLE IF EXISTS TbTag');
		self.execute("""
			CREATE TABLE TbTag (
				f_id INT NOT NULL AUTO_INCREMENT,
				f_name VARCHAR(40) NOT NULL,
				f_description VARCHAR(256) NOT NULL,
				PRIMARY KEY(f_id),
				UNIQUE KEY f_name (f_name)
			) ENGINE=InnoDB
		""")
		self.execute("""
			CREATE TABLE TbTagRelations (
				f_parent_tag INT NOT NULL,
				f_child_tag INT NOT NULL,
				KEY f_parent_tag (f_parent_tag),
				KEY f_child_tag (f_child_tag),
				CONSTRAINT FOREIGN KEY(f_parent_tag) REFERENCES TbTag(f_id),
				CONSTRAINT FOREIGN KEY(f_child_tag) REFERENCES TbTag(f_id)
			) ENGINE=InnoDB
		""")
		self.execute("""
			CREATE TABLE TbFile (
				f_id INT NOT NULL AUTO_INCREMENT,
				f_name VARCHAR(256) NOT NULL,
				f_mtime DATETIME NOT NULL,
				f_parent INT,
				PRIMARY KEY(f_id),
				UNIQUE KEY f_name_id (f_id,f_name),
				KEY f_parent (f_parent),
				CONSTRAINT FOREIGN KEY(f_parent) REFERENCES TbFile(f_id)
			) ENGINE=InnoDB
		""")
		self.execute("""
			CREATE TABLE TbFileTag (
				f_file INT NOT NULL,
				f_tag INT NOT NULL,
				KEY f_file (f_file),
				KEY f_tag (f_tag),
				CONSTRAINT FOREIGN KEY(f_file) REFERENCES TbFile(f_id),
				CONSTRAINT FOREIGN KEY(f_tag) REFERENCES TbTag(f_id)
			) ENGINE=InnoDB
		""")
		self.disconnect()
	def scan(self):
		directory=tagger.config.ns_mgr.p_dir
