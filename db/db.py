import sqlite3
import sys
import datetime

from conf.conf import path_to_db

class DefaultDB():
    def __init__(self):
        self.conn = sqlite3.connect(path_to_db + "dictionary.db")
        self.cur = self.conn.cursor()
        queries = [
            "SELECT 'ok' FROM sqlite_master WHERE type='table' AND name='words'",
            "SELECT 'ok' FROM sqlite_master WHERE type='table' AND name='word_groups'",
            "SELECT 'ok' FROM sqlite_master WHERE type='table' AND name='words__word_groups'",
            "SELECT 'ok' FROM sqlite_master WHERE type='table' AND name='rules'",
        ]

        check_if_table_exists_res = []
        for i in queries:
            self.cur.execute(i)
            check_if_table_exists_res.append(self.cur.fetchone())
        if not None in check_if_table_exists_res:
            return

        sql = '''\
        CREATE TABLE IF NOT EXISTS words (
            _id INTEGER PRIMARY KEY AUTOINCREMENT,
            word_en TEXT NOT NULL,
            word_ru TEXT NOT NULL,
            time_added INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS word_groups (
            _id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS words__word_groups (
            word_id INTEGER,
            word_group_id INTEGER,
            FOREIGN KEY(word_id) REFERENCES words(word_id),
            FOREIGN KEY(word_group_id) REFERENCES words(word_group_id)
        );
        CREATE TABLE IF NOT EXISTS rules (
            _id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            rule TEXT NOT NULL
        );
        '''
        try:
            self.cur.executescript(sql)
        except sqlite3.DatabaseError as err:
            print("Error: ", err)
            sys.exit()

        print("DB successfully created")
        return

    def add_word(self, en, ru):
        ts = datetime.datetime.now().timestamp()
        query = "INSERT INTO words (word_en, word_ru, time_added) VALUES(?,?,?)"
        data = (en, ru, int(ts),)
        self.cur.execute(query, data)
        self.conn.commit()

    def update_word(self, id, en, ru):
        query = "UPDATE words SET word_en = ?, word_ru = ? WHERE _id = ?"
        data = (en, ru, id,)
        self.cur.execute(query, data)
        self.conn.commit()

    def delete_word(self, id):
        query = "DELETE FROM words WHERE _id = ?"
        data = (id,)
        self.cur.execute(query, data)
        self.conn.commit()

    def get_word(self, id):
        query = "SELECT * FROM words where _id = ?"
        data = (id,)
        self.cur.execute(query, data)
        return self.cur.fetchone()

    def get_full_dict(self):
        query = "SELECT * FROM words"
        self.cur.execute(query)
        return self.cur.fetchall()
