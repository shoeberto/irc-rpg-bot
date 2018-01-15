import sqlite3
import config

class Database(object):
    conn = None

    def __init__(self):
        self.conn = sqlite3.connect(config.database_location)
        self.conn.row_factory = sqlite3.Row

    def query(self, query, params = []):
        cursor = self.conn.cursor()

        if len(params) > 0:
            cursor.execute(query.decode('utf-8'), params)
        else:
            cursor.execute(query.decode('utf-8'))

        return cursor

    def fetchall(self, cursor):
        return cursor.fetchall()

    def fetchone(self, cursor):
        return cursor.fetchone()

    def commit(self):
        self.conn.commit()
