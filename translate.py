from googletrans import Translator

from db import DefaultDB

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
                self.db.add_word_to_dictionary(translated, text)
            else:
                self.db.add_word_to_dictionary(text, translated)
        except Exception as err:
            print("Translate Error :", err)
            return str(err)

        return translated


    def show_dictionary(self):
        try:
            return self.db.get_dictionary()
        except Exception as err:
            return str(err)

    def delete_from_dictionary(self, id):
        try:
            return self.db.delete_word_from_dictionary(id)
        except Exception as err:
            return str(err)
