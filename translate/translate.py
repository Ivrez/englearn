import sys

from googletrans import Translator

from db.db import DefaultDB
from db_mongo.db import DefaultMongoDB

class Translate():
    def __init__(self):
        self.translator = Translator()
        self.db = DefaultMongoDB()
        #self.db = DefaultDB()

    def add_word(self, en, ru):
        try:
            self.db.add_word(en, ru)
        except Exception as err:
            return str(err)

    def translate(self, text, add_to_dict=False):
        dest = 'ru'
        src = 'en'

        lang = self.translator.detect(text)
        # due to some language recognition problems
        if lang.lang in ['ru', 'bg', 'tj', 'sr', 'uk']:
            src = 'ru'
            dest = 'en'
        try:
            translated = self.translator.translate(text, dest=dest, src=src)
            if add_to_dict:
                if src == 'ru':
                    self.add_word(translated.text, text)
                else:
                    self.add_word(text, translated.text)
        except Exception as err:
            print("Translate Error : " + str(err))
            sys.exit()


        return translated

    def get_full_dict(self):
        try:
            return self.db.get_full_dict()
        except Exception as err:
            return str(err)

    def get_word(self, id):
        try:
            return self.db.get_word(id)
        except Exception as err:
            return str(err)

    def delete_word(self, id):
        try:
            return self.db.delete_word(id)
        except Exception as err:
            return str(err)
