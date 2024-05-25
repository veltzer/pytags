import os

import mysql.connector

import pytags.config

Q_INSERT = "INSERT INTO TbFile (f_name, f_mtime, f_parent) VALUES(\"%s\", FROM_UNIXTIME(%s), %s)"


class Mgr:
    def __init__(self):
        self.tags = {}

    def connect(self):
        return mysql.connector.Connect({})

    def connectNodb(self):
        return mysql.connector.Connect({})

    def get_row(self, connection, query):
        cr = Mgr.getCursor(connection)
        cr.execute(query)
        row = cr.fetchone()
        cr.close()
        return row

    @staticmethod
    def debug(string):
        if pytags.config.ns_op["p_debug"]:
            print(string)

    def execute(self, connection, stmt, commit):
        """ Run the given query, commit changes """
        if pytags.config.ns_op["p_sql_debug"]:
            print(f"doing {stmt}")
        cr = Mgr.getCursor(connection)
        num_affected_rows = cr.execute(stmt)
        cr.close()
        if commit:
            connection.commit()
        return num_affected_rows

    def error(self, msg):
        raise ValueError(msg)

    def find_id_in_folder(self, conn, folder_id, name, curname, raiseError):
        """ find the id of a file named name in folder with db id id """
        if folder_id is None:
            query = "SELECT f_id from TbFile WHERE f_parent IS NULL"
        else:
            query = f"SELECT f_id from TbFile WHERE f_name=\"{name}\" AND f_parent={folder_id}"
        row = self.get_row(conn, query)
        if row is None:
            if raiseError:
                if folder_id is None:
                    msg = "cannot find root folder"
                else:
                    msg = f"cannot find folder {name} in {curname}"
                raise ValueError(msg)
            return None
        return row[0]

    def createFolder(self, conn, folder_id, name, curname):
        """ create a folder """
        if folder_id is None:
            query = Q_INSERT % (name, os.path.getmtime(curname), "NULL")
        else:
            query = Q_INSERT % (name, os.path.getmtime(curname), folder_id)
        self.execute(conn, query, False)
        return conn.insert_id()

    def showconfig(self):
        pytags.config.show()

    def testconnect(self):
        with self.connect():
            pass

    @staticmethod
    def getCursor(conn):
        return conn.cursor()

    def loadTags(self):
        # the dictionary for the tags
        self.tags = {}
        conn = self.connect()
        with conn:
            cr = Mgr.getCursor(conn)
            cr.execute("SELECT f_id,f_name,f_description from TbTag")
            row = cr.fetchone()
            while row is not None:
                # name to id mapping...
                f_id = row["f_id"]
                f_name = row["f_name"]
                self.tags[f_name] = f_id
                Mgr.debug(f"inserting key {f_name} value {f_id}")
                row = cr.fetchone()
            cr.close()

    def dropTables(self, conn):
        self.execute(conn, "DROP DATABASE IF EXISTS TbFileTag", False)
        self.execute(conn, "DROP TABLE IF EXISTS TbFileTag", False)
        self.execute(conn, "DROP TABLE IF EXISTS TbFile", False)
        self.execute(conn, "DROP TABLE IF EXISTS TbTagRelations", False)
        self.execute(conn, "DROP TABLE IF EXISTS TbTag", False)

    def createdb(self):
        # remove the old database if force is in place
        if pytags.config.ns_op["p_force"]:
            try:
                conn = self.connect()
                print("found database - removing it...")
                with conn:
                    p_db = pytags.config.ns_db["p_db"]
                    query = f"DROP DATABASE IF EXISTS {p_db}"
                    self.execute(conn, query, True)
            except mysql.connector.Error:
                print("no previous database detected")
        # create the database
        conn = self.connectNodb()
        with conn:
            print("creating the empty database...")
            p_db = pytags.config.ns_db["p_db"]
            query = f"CREATE DATABASE {p_db}"
            self.execute(conn, query, True)
        # connect to a clean database
        conn = self.connect()
        with conn:
            print("creating the tables...")
            self.execute(conn, """
                CREATE TABLE TbTag (
                    f_id INT NOT NULL AUTO_INCREMENT,
                    f_name VARCHAR(40) NOT NULL,
                    f_description VARCHAR(256) NOT NULL,
                    PRIMARY KEY(f_id),
                    UNIQUE KEY f_name (f_name)
                ) ENGINE=InnoDB
            """, False)
            self.execute(conn, """
                CREATE TABLE TbTagRelations (
                    f_parent_tag INT NOT NULL,
                    f_child_tag INT NOT NULL,
                    KEY f_parent_tag (f_parent_tag),
                    KEY f_child_tag (f_child_tag),
                    CONSTRAINT FOREIGN KEY(f_parent_tag) REFERENCES TbTag(f_id),
                    CONSTRAINT FOREIGN KEY(f_child_tag) REFERENCES TbTag(f_id)
                ) ENGINE=InnoDB
            """, False)
            self.execute(conn, """
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
            """, False)
            self.execute(conn, """
                CREATE TABLE TbFileTag (
                    f_file INT NOT NULL,
                    f_tag INT NOT NULL,
                KEY f_file (f_file),
                KEY f_tag (f_tag),
                CONSTRAINT FOREIGN KEY(f_file) REFERENCES TbFile(f_id),
                CONSTRAINT FOREIGN KEY(f_tag) REFERENCES TbTag(f_id)
                ) ENGINE=InnoDB
            """, False)
            conn.commit()
            # self.execute(conn, """
            #    INSERT INTO TbFile (f_name,f_mtime,f_parent) VALUES("%s",FROM_UNIXTIME(%s),%s)
            #    """ % ("/",os.path.getmtime("/"),1),False)

    def scan(self):
        # first load all the current tags
        self.loadTags()
        # now add the directory if its not there...
        # directory = pytags.config.ns_mgr.p_dir

    def search(self):
        conn = self.connect()
        with conn:
            directory = pytags.config.ns_mgr["p_dir"]
            if not os.path.isdir(directory):
                self.error(directory + " is not a directory")
            # turn the folder into absolute path
            directory = os.path.abspath(directory)
            curname = ""
            folder_id = None
            for comp in directory.split("/"):
                curname += "/" + comp
                folder_id = self.find_id_in_folder(conn, folder_id, comp, curname, True)

    def taglist(self):
        conn = self.connect()
        with conn:
            cr = Mgr.getCursor(conn)
            cr.execute("SELECT f_name from TbTag")
            row = cr.fetchone()
            while row is not None:
                print(row["f_name"])
                row = cr.fetchone()
            cr.close()

    def raiseexception(self):
        raise ValueError("this is the exception message")

    def insertdir(self):
        conn = self.connect()
        with conn:
            directory = pytags.config.ns_mgr["p_dir"]
            if not os.path.isdir(directory):
                self.error(directory + " is not a directory")
            # turn the folder into absolute path
            directory = os.path.abspath(directory)
            curname = ""
            folder_id = None
            find = True
            for comp in directory.split("/"):
                curname += "/" + comp
                if find:
                    nextid = self.find_id_in_folder(conn, folder_id, comp, curname, False)
                    if nextid is None:
                        find = False
                    else:
                        folder_id = nextid
                if not find:
                    folder_id = self.createFolder(conn, folder_id, comp, curname)
            if not find:
                conn.commit()

    def inserttag(self):
        conn = self.connect()
        with conn:
            tagname = "tagname"
            tagdescription = "tagdescription"
            query = f"INSERT INTO TbTag (f_name,f_description) VALUES(\"{tagname}\",\"{tagdescription}\")"
            self.execute(conn, query, True)

    def clean(self):
        if not pytags.config.ns_op["p_force"]:
            raise ValueError("must pass --force")
        conn = self.connect()
        with conn:
            self.execute(conn, "SET foreign_key_checks = 0", False)
            self.execute(conn, "DELETE FROM TbFileTag", False)
            self.execute(conn, "DELETE FROM TbFile", False)
            self.execute(conn, "DELETE FROM TbTagRelations", False)
            self.execute(conn, "DELETE FROM TbTag", False)
            self.execute(conn, "ALTER TABLE TbFileTag AUTO_INCREMENT = 1", False)
            self.execute(conn, "ALTER TABLE TbFile AUTO_INCREMENT = 1", False)
            self.execute(conn, "ALTER TABLE TbTagRelations AUTO_INCREMENT = 1", False)
            self.execute(conn, "ALTER TABLE TbTag AUTO_INCREMENT = 1", False)
            self.execute(conn, "SET foreign_key_checks = 1", False)
            conn.commit()
