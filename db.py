import sqlite3
import sys
import datetime

class DefaultDB():
    def __init__(self):
        self.conn = sqlite3.connect("dictionary.db")
        self.cur = self.conn.cursor()
        queries = [
            "SELECT 'ok' FROM sqlite_master WHERE type='table' AND name='words'",
            "SELECT 'ok' FROM sqlite_master WHERE type='table' AND name='word_groups'",
            "SELECT 'ok' FROM sqlite_master WHERE type='table' AND name='rules'",
        ]

        res = []
        for i in queries:
            self.cur.execute(i)
            res.append(self.cur.fetchone())
        if not None in res:
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
        CREATE TABLE words__word_groups (
            word_id INTEGER,
            word_group_id INTEGER,
            FOREIGN KEY(word_id) REFERENCES words(word_id),
            FOREIGN KEY(word_group_id) REFERENCES words(word_group_id)
        );
        CREATE TABLE IF NOT EXISTS rules (
            _id INTEGER PRIMARY KEY,
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

    def add_word_to_dictionary(self, en, ru):
        ts = datetime.datetime.now().timestamp()
        query = "INSERT INTO words (word_en, word_ru, time_added) VALUES(?,?,?)"
        data = (en, ru, int(ts),)
        self.cur.execute(query, data)

    def update_word_to_dictionary(self, id, en, ru):
        query = "UPDATE words SET word_en = ?, word_ru = ? WHERE id = ?"
        data = (en, ru, id,)
        self.cur.execute(query, data)

    def show_dictionary(self):
        query = "SELECT * FROM words"
        self.cur.execute(query)
        print(self.cur.fetchone())
