from googletrans import Translator


class Translate():
    def __init__(self):
        self.translator = Translator()

    def translate(self, text):
        dest = 'ru'
        src = 'en'

        lang = self.translator.detect(text)
        # due to some language recognition problems
        if lang.lang in ['ru', 'bg', 'tj', 'sr', 'uk']:
            src = 'ru'
            dest = 'en'
        translated = self.translator.translate(text, dest=dest, src=src)

        return translated.text
