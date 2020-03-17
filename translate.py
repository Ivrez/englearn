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
            translated = self.translator.translate(text, dest=dest, src=src)
            translated = translated.text
            if src == 'ru':
                self.db.add_word_to_dictionary(translated, text)
            else:
                self.db.add_word_to_dictionary(text, translated)
        except Exception as e:
            print("Error :", e)
            return str(e)

        return translated


    def show_dictionary(self):
        return self.db.get_dictionary()
