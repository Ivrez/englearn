import ssl

from pymongo import MongoClient

from bson.objectid import ObjectId

class DefaultMongoDB():
    def __init__(self):
        conn = ''

        client = MongoClient(conn)
        #client = MongoClient(conn, ssl_cert_reqs=ssl.CERT_NONE)

        self.db = client.englearn

    def add_word(self, word_eng, word_rus):
        data = {
                'word_eng': word_eng,
                'word_rus': word_rus,
        }
        self.db.words.insert(data)

    def get_full_dict(self):
        data = self.db.words.find({})
        return data

    def update_word(self, word_id, word_eng, word_rus):
        data = {
                'word_eng': word_eng,
                'word_rus': word_rus,
        }
        db.test.update_one({'_id': word_id}, data)

    def get_word(self, word_id):
        data = self.db.words.find_one({'_id': word_id})
        return data

    def delete_word(self, word_id):
        data = self.db.words.delete_one({'_id': ObjectId(word_id)})
        return data

