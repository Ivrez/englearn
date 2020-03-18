from googletrans import Translator

from db.db import DefaultDB

class Translate():

    def __init__(self):
        self.translator = Translator()
        self.db = DefaultDB()

    def translate(self, text):
        dest = 'ru'
        src = 'en'

        lang = self.translator.detect(text)
        # due to some language recognition problems
        if lang.lang in ['ru', 'bg', 'tj', 'sr', 'uk']:
            src = 'ru'
            dest = 'en'

        try:
            translated = self.translator.translate(text, dest=dest, src=src).text
            if src == 'ru':
                self.db.add_word(translated, text)
            else:
                self.db.add_word(text, translated)
        except Exception as err:
            print("Translate Error :", err)
            return str(err)

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
