import tagger.config
import MySQLdb
import warnings
import os

class Mgr:
    def __init__(self):
        # remove mysql warnings...
        if tagger.config.ns_mgr.p_suppress_warnings:
            warnings.filterwarnings('ignore', category = MySQLdb.Warning)
    ''' helpers '''
    def connect(self):
        return MySQLdb.connect(
            db=tagger.config.ns_db.p_db,
            host=tagger.config.ns_db.p_host,
            port=tagger.config.ns_db.p_port,
            user=tagger.config.ns_db.p_user,
            passwd=tagger.config.ns_db.p_password,
        )
    def connectNodb(self):
        return MySQLdb.connect(
            db='mysql',
            host=tagger.config.ns_db.p_host,
            port=tagger.config.ns_db.p_port,
            user=tagger.config.ns_db.p_user,
            passwd=tagger.config.ns_db.p_password,
        )
    def get_row(self,connection,query):
        cr=Mgr.getCursor(connection)
        cr.execute(query)
        row=cr.fetchone()
        cr.close()
        return row
    @staticmethod
    def debug(string):
        if tagger.config.ns_op.p_debug:
            print string
    ''' Run the given query, commit changes '''
    def execute(self,connection,stmt,commit):
        if tagger.config.ns_op.p_sql_debug:
            print 'doing',stmt
        cr=Mgr.getCursor(connection)
        num_affected_rows=cr.execute(stmt)
        cr.close()
        if commit:
            connection.commit()
        return num_affected_rows
    def error(self,msg):
        raise ValueError(msg)
    ''' find the id of a file named name in folder with db id id '''
    def find_id_in_folder(self,conn,id,name,curname,raiseError):
        if id is None:
            query='SELECT f_id from TbFile WHERE f_parent IS NULL'
        else:
            query='SELECT f_id from TbFile WHERE f_name="%s" AND f_parent=%d' % (name,id)
        row=self.get_row(conn,query)
        if row is None:
            if raiseError:
                if id is None:
                    msg='cannot find root folder'
                else:
                    msg='cannot find folder '+name+' in '+curname
                raise ValueError(msg)
            else:
                return None
        else:
            return row[0]
    ''' create a folder '''
    def createFolder(self,conn,id,name,curname):
        if id is None:
            query='INSERT INTO TbFile (f_name,f_mtime,f_parent) VALUES("%s",FROM_UNIXTIME(%s),%s)' % (name,os.path.getmtime(curname),'NULL')
        else:
            query='INSERT INTO TbFile (f_name,f_mtime,f_parent) VALUES("%s",FROM_UNIXTIME(%s),%s)' % (name,os.path.getmtime(curname),id)
        self.execute(conn,query,False)
        return conn.insert_id();
    ''' ops that can be launched from the command line '''
    def showconfig(self):
        tagger.config.show()
    def testconnect(self):
        with self.connect():
            pass
    @staticmethod
    def getCursor(conn):
        #return conn.cursor()
        return conn.cursor(MySQLdb.cursors.DictCursor)
    def loadTags(self):
        # the dictionary for the tags
        self.tags={}
        conn=self.connect()
        with conn:
            cr=Mgr.getCursor(conn)
            cr.execute('SELECT f_id,f_name,f_description from TbTag')
            row=cr.fetchone()
            while row is not None:
                # name to id mapping...
                self.tags[row['f_name']]=row['f_id']
                Mgr.debug('inserting key %s value %s' % (row['f_name'],row['f_id']))
                row=cr.fetchone()
            cr.close()
    def dropTables(self,conn):
        self.execute(conn,'DROP DATABASE IF EXISTS TbFileTag',False)
        self.execute(conn,'DROP TABLE IF EXISTS TbFileTag',False)
        self.execute(conn,'DROP TABLE IF EXISTS TbFile',False)
        self.execute(conn,'DROP TABLE IF EXISTS TbTagRelations',False)
        self.execute(conn,'DROP TABLE IF EXISTS TbTag',False)
    def createdb(self):
        # remove the old database if force is in place
        if tagger.config.ns_op.p_force:
            try:
                conn=self.connect()
                print 'found database - removing it...'
                with conn:
                    query='DROP DATABASE IF EXISTS %s' % (tagger.config.ns_db.p_db)
                    self.execute(conn,query,True)
            except:
                print 'no previous database detected'
        # create the database
        conn=self.connectNodb()
        with conn:
            print 'creating the empty database...'
            query='CREATE DATABASE %s' % (tagger.config.ns_db.p_db)
            self.execute(conn,query,True)
        # connect to a clean database
        conn=self.connect()
        with conn:
            print 'creating the tables...'
            self.execute(conn,'''
                CREATE TABLE TbTag (
                    f_id INT NOT NULL AUTO_INCREMENT,
                    f_name VARCHAR(40) NOT NULL,
                    f_description VARCHAR(256) NOT NULL,
                    PRIMARY KEY(f_id),
                    UNIQUE KEY f_name (f_name)
                ) ENGINE=InnoDB
            ''',False)
            self.execute(conn,'''
                CREATE TABLE TbTagRelations (
                    f_parent_tag INT NOT NULL,
                    f_child_tag INT NOT NULL,
                    KEY f_parent_tag (f_parent_tag),
                    KEY f_child_tag (f_child_tag),
                    CONSTRAINT FOREIGN KEY(f_parent_tag) REFERENCES TbTag(f_id),
                    CONSTRAINT FOREIGN KEY(f_child_tag) REFERENCES TbTag(f_id)
                ) ENGINE=InnoDB
            ''',False)
            self.execute(conn,'''
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
            ''',False)
            self.execute(conn,'''
                CREATE TABLE TbFileTag (
                    f_file INT NOT NULL,
                    f_tag INT NOT NULL,
                KEY f_file (f_file),
                KEY f_tag (f_tag),
                CONSTRAINT FOREIGN KEY(f_file) REFERENCES TbFile(f_id),
                CONSTRAINT FOREIGN KEY(f_tag) REFERENCES TbTag(f_id)
                ) ENGINE=InnoDB
            ''',False)
            conn.commit()
            #self.execute(conn,'''
            #    INSERT INTO TbFile (f_name,f_mtime,f_parent) VALUES("%s",FROM_UNIXTIME(%s),%s)
            #    ''' % ('/',os.path.getmtime('/'),1)
            #,False)
    def scan(self):
        # first load all the current tags
        self.loadTags()
        # now add the directory if it's not there...
        directory=tagger.config.ns_mgr.p_dir
    def search(self):
        conn=self.connect()
        with conn:
            directory=tagger.config.ns_mgr.p_dir
            if not os.path.isdir(directory):
                self.error(directory+' is not a directory')
            # turn the folder into absolute path
            directory=os.path.abspath(directory)
            curname=''
            id=None
            for comp in directory.split('/'):
                curname+='/'+comp
                id=self.find_id_in_folder(conn,id,comp,curname,True)
    def taglist(self):
        conn=self.connect()
        with conn:
            cr=Mgr.getCursor(conn)
            cr.execute('SELECT f_name from TbTag')
            row=cr.fetchone()
            while row is not None:
                print row['f_name']
                row=cr.fetchone()
            cr.close()
    def raiseexception(self):
        raise ValueError('this is the exception message')
    def insertdir(self):
        conn=self.connect()
        with conn:
            directory=tagger.config.ns_mgr.p_dir
            if not os.path.isdir(directory):
                self.error(directory+' is not a directory')
            # turn the folder into absolute path
            directory=os.path.abspath(directory)
            curname=''
            id=None
            find=True
            for comp in directory.split('/'):
                curname+='/'+comp
                if find:
                    nextid=self.find_id_in_folder(conn,id,comp,curname,False)
                    if nextid is None:
                        find=False
                    else:
                        id=nextid
                if not find:
                    id=self.createFolder(conn,id,comp,curname)
            if not find:
                conn.commit()

    def inserttag(self):
        conn=self.connect()
        with conn:
            query='INSERT INTO TbTag (f_name,f_description) VALUES("%s","%s")' % ('tagname','tagdescription')
            self.execute(conn,query,True)
    def clean(self):
        if not tagger.config.ns_op.p_force:
            raise ValueError('must pass --force')
        conn=self.connect()
        with conn:
            self.execute(conn,'SET foreign_key_checks = 0',False)
            self.execute(conn,'DELETE FROM TbFileTag',False)
            self.execute(conn,'DELETE FROM TbFile',False)
            self.execute(conn,'DELETE FROM TbTagRelations',False)
            self.execute(conn,'DELETE FROM TbTag',False)
            self.execute(conn,'ALTER TABLE TbFileTag AUTO_INCREMENT = 1',False)
            self.execute(conn,'ALTER TABLE TbFile AUTO_INCREMENT = 1',False)
            self.execute(conn,'ALTER TABLE TbTagRelations AUTO_INCREMENT = 1',False)
            self.execute(conn,'ALTER TABLE TbTag AUTO_INCREMENT = 1',False)
            self.execute(conn,'SET foreign_key_checks = 1',False)
            conn.commit()
