import sqlite3

conn = sqlite3.connect("dictionary.db")
cur = conn.cursor()

sql = '''\
CREATE TABLE words (
    word_id INTEGER PRIMARY KEY AUTOINCREMENT,
    word_en TEXT NOT NULL,
    word_ru TEXT NOT NULL,
    word_rating INTEGER NOT NULL,
    time_added INTEGER NOT NULL
);
CREATE TABLE word_groups (
    word_group_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL
);
'''

try:
    cur.executescript(sql)
except sqlite3.DatabaseError as err:
    print("Error: ", err)
    sys.exit()

print("Successfully executed")
