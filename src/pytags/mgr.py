"""
mgr.py
"""

import contextlib
import os
from typing import TYPE_CHECKING

import mysql.connector

import pytags.config

if TYPE_CHECKING:
    from mysql.connector.abstracts import MySQLConnectionAbstract
    from mysql.connector.pooling import PooledMySQLConnection

Q_INSERT = "INSERT INTO TbFile (f_name, f_mtime, f_parent) VALUES(\"%s\", FROM_UNIXTIME(%s), %s)"


class Mgr:
    def __init__(self) -> None:
        self.tags = {}

    def connect(self) -> MySQLConnectionAbstract | PooledMySQLConnection:
        return mysql.connector.Connect({})

    def connect_nodb(self) -> MySQLConnectionAbstract | PooledMySQLConnection:
        return mysql.connector.Connect({})

    def get_row(self, connection: MySQLConnectionAbstract | PooledMySQLConnection, query: str):
        cr = Mgr.get_cursor(connection)
        cr.execute(query)
        row = cr.fetchone()
        cr.close()
        return row

    @staticmethod
    def debug(string: str) -> None:
        if pytags.config.ns_op["p_debug"]:
            print(string)

    def execute(self, connection: MySQLConnectionAbstract | PooledMySQLConnection, stmt: str, *, commit: bool):
        """ Run the given query, commit changes """
        if pytags.config.ns_op["p_sql_debug"]:
            print(f"doing {stmt}")
        cr = Mgr.get_cursor(connection)
        num_affected_rows = cr.execute(stmt)
        cr.close()
        if commit:
            connection.commit()
        return num_affected_rows

    def error(self, msg: str):
        raise ValueError(msg)

    def find_id_in_folder(self, conn: MySQLConnectionAbstract | PooledMySQLConnection, folder_id: int | None, name: str, curname: str, *, raise_error: bool):
        """ find the id of a file named name in folder with db id id """
        if folder_id is None:
            query = "SELECT f_id from TbFile WHERE f_parent IS NULL"
        else:
            query = f"SELECT f_id from TbFile WHERE f_name=\"{name}\" AND f_parent={folder_id}"
        row = self.get_row(conn, query)
        if row is None:
            if raise_error:
                msg = "cannot find root folder" if folder_id is None else f"cannot find folder {name} in {curname}"
                raise ValueError(msg)
            return None
        return row["f_id"]

    def create_folder(self, conn: MySQLConnectionAbstract | PooledMySQLConnection, folder_id: int | None, name: str, curname: str):
        """ create a folder """
        if folder_id is None:
            query = Q_INSERT % (name, os.path.getmtime(curname), "NULL")
        else:
            query = Q_INSERT % (name, os.path.getmtime(curname), folder_id)
        cr = Mgr.get_cursor(conn)
        cr.execute(query)
        new_id = cr.lastrowid
        cr.close()
        return new_id

    def showconfig(self) -> None:
        pytags.config.show()

    def testconnect(self) -> None:
        with contextlib.closing(self.connect()):
            pass

    @staticmethod
    def get_cursor(conn: MySQLConnectionAbstract | PooledMySQLConnection):
        return conn.cursor(dictionary=True)

    def load_tags(self) -> None:
        # the dictionary for the tags
        self.tags = {}
        conn = self.connect()
        with contextlib.closing(conn):
            cr = Mgr.get_cursor(conn)
            cr.execute("SELECT f_id,f_name,f_description from TbTag")
            row = cr.fetchone()
            while isinstance(row, dict):
                # name to id mapping...
                f_id = row["f_id"]
                f_name = row["f_name"]
                self.tags[f_name] = f_id
                Mgr.debug(f"inserting key {f_name} value {f_id}")
                row = cr.fetchone()
            cr.close()

    def drop_tables(self, conn: MySQLConnectionAbstract | PooledMySQLConnection) -> None:
        self.execute(conn, "DROP DATABASE IF EXISTS TbFileTag", commit=False)
        self.execute(conn, "DROP TABLE IF EXISTS TbFileTag", commit=False)
        self.execute(conn, "DROP TABLE IF EXISTS TbFile", commit=False)
        self.execute(conn, "DROP TABLE IF EXISTS TbTagRelations", commit=False)
        self.execute(conn, "DROP TABLE IF EXISTS TbTag", commit=False)

    def createdb(self) -> None:
        # remove the old database if force is in place
        if pytags.config.ns_op["p_force"]:
            try:
                conn = self.connect()
                print("found database - removing it...")
                with contextlib.closing(conn):
                    p_db = pytags.config.ns_db["p_db"]
                    query = f"DROP DATABASE IF EXISTS {p_db}"
                    self.execute(conn, query, commit=True)
            except mysql.connector.Error:
                print("no previous database detected")
        # create the database
        conn = self.connect_nodb()
        with contextlib.closing(conn):
            print("creating the empty database...")
            p_db = pytags.config.ns_db["p_db"]
            query = f"CREATE DATABASE {p_db}"
            self.execute(conn, query, commit=True)
        # connect to a clean database
        conn = self.connect()
        with contextlib.closing(conn):
            print("creating the tables...")
            self.execute(conn, """
                CREATE TABLE TbTag (
                    f_id INT NOT NULL AUTO_INCREMENT,
                    f_name VARCHAR(40) NOT NULL,
                    f_description VARCHAR(256) NOT NULL,
                    PRIMARY KEY(f_id),
                    UNIQUE KEY f_name (f_name)
                ) ENGINE=InnoDB
            """, commit=False)
            self.execute(conn, """
                CREATE TABLE TbTagRelations (
                    f_parent_tag INT NOT NULL,
                    f_child_tag INT NOT NULL,
                    KEY f_parent_tag (f_parent_tag),
                    KEY f_child_tag (f_child_tag),
                    CONSTRAINT FOREIGN KEY(f_parent_tag) REFERENCES TbTag(f_id),
                    CONSTRAINT FOREIGN KEY(f_child_tag) REFERENCES TbTag(f_id)
                ) ENGINE=InnoDB
            """, commit=False)
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
            """, commit=False)
            self.execute(conn, """
                CREATE TABLE TbFileTag (
                    f_file INT NOT NULL,
                    f_tag INT NOT NULL,
                KEY f_file (f_file),
                KEY f_tag (f_tag),
                CONSTRAINT FOREIGN KEY(f_file) REFERENCES TbFile(f_id),
                CONSTRAINT FOREIGN KEY(f_tag) REFERENCES TbTag(f_id)
                ) ENGINE=InnoDB
            """, commit=False)
            conn.commit()
            # self.execute(conn, """
            #    INSERT INTO TbFile (f_name,f_mtime,f_parent) VALUES("%s",FROM_UNIXTIME(%s),%s)
            #    """ % ("/",os.path.getmtime("/"),1),False)

    def scan(self) -> None:
        # first load all the current tags
        self.load_tags()

    def search(self) -> None:
        conn = self.connect()
        with contextlib.closing(conn):
            directory = pytags.config.ns_mgr["p_dir"]
            if directory is None:
                self.error("no directory was given")
            if not os.path.isdir(directory):
                self.error(f"{directory} is not a directory")
            # turn the folder into absolute path
            directory = os.path.abspath(directory)
            curname = ""
            folder_id = None
            for comp in directory.split("/"):
                curname += "/" + comp
                folder_id = self.find_id_in_folder(conn, folder_id, comp, curname, raise_error=True)

    def taglist(self) -> None:
        conn = self.connect()
        with contextlib.closing(conn):
            cr = Mgr.get_cursor(conn)
            cr.execute("SELECT f_name from TbTag")
            row = cr.fetchone()
            while isinstance(row, dict):
                print(row["f_name"])
                row = cr.fetchone()
            cr.close()

    def raiseexception(self):
        raise ValueError("this is the exception message")

    def insertdir(self) -> None:
        conn = self.connect()
        with contextlib.closing(conn):
            directory = pytags.config.ns_mgr["p_dir"]
            if directory is None:
                self.error("no directory was given")
            if not os.path.isdir(directory):
                self.error(f"{directory} is not a directory")
            # turn the folder into absolute path
            directory = os.path.abspath(directory)
            curname = ""
            folder_id = None
            find = True
            for comp in directory.split("/"):
                curname += "/" + comp
                if find:
                    nextid = self.find_id_in_folder(conn, folder_id, comp, curname, raise_error=False)
                    if nextid is None:
                        find = False
                    else:
                        folder_id = nextid
                if not find:
                    folder_id = self.create_folder(conn, folder_id, comp, curname)
            if not find:
                conn.commit()

    def inserttag(self) -> None:
        conn = self.connect()
        with contextlib.closing(conn):
            tagname = "tagname"
            tagdescription = "tagdescription"
            query = f"INSERT INTO TbTag (f_name,f_description) VALUES(\"{tagname}\",\"{tagdescription}\")"
            self.execute(conn, query, commit=True)

    def clean(self) -> None:
        if not pytags.config.ns_op["p_force"]:
            raise ValueError("must pass --force")
        conn = self.connect()
        with contextlib.closing(conn):
            self.execute(conn, "SET foreign_key_checks = 0", commit=False)
            self.execute(conn, "DELETE FROM TbFileTag", commit=False)
            self.execute(conn, "DELETE FROM TbFile", commit=False)
            self.execute(conn, "DELETE FROM TbTagRelations", commit=False)
            self.execute(conn, "DELETE FROM TbTag", commit=False)
            self.execute(conn, "ALTER TABLE TbFileTag AUTO_INCREMENT = 1", commit=False)
            self.execute(conn, "ALTER TABLE TbFile AUTO_INCREMENT = 1", commit=False)
            self.execute(conn, "ALTER TABLE TbTagRelations AUTO_INCREMENT = 1", commit=False)
            self.execute(conn, "ALTER TABLE TbTag AUTO_INCREMENT = 1", commit=False)
            self.execute(conn, "SET foreign_key_checks = 1", commit=False)
            conn.commit()
