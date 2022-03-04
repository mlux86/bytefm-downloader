import sqlite3
from os.path import exists


class DownloadsDatabase:
    INIT_FILE = 'downloads.sql'
    DB_FILE = 'downloads.db'

    def __init__(self, base_dir):
        file = f'{base_dir}/{self.DB_FILE}'
        if exists(file):
            self.conn = sqlite3.connect(file)
        else:
            self.conn = sqlite3.connect(file)
            self.create_db(base_dir)

    def create_db(self, base_dir):
        file = f'{base_dir}/{self.INIT_FILE}'
        with open(file, 'r') as sql_file:
            sql = sql_file.read()
            c = self.conn.cursor()
            c.executescript(sql)
            self.conn.commit()

    def execute_db(self, statement, args):
        c = self.conn.cursor()
        c.execute(statement, args)
        result = c.fetchall()
        self.conn.commit()
        return result

    def get_count(self, show, url):
        return self.execute_db("SELECT COUNT(url) FROM downloads WHERE program = ? AND url = ?;", (show, url))[0][0]

    def log_download(self, show, url):
        self.execute_db("INSERT INTO downloads (program, url) VALUES (?, ?);", (show, url))

    def close(self):
        self.conn.close()
