from __future__ import print_function

from builtins import str
from builtins import input
from builtins import object
from menu import Menu

from datetime import datetime
from translate.translate import Translate

class CLI():
    def __init__(self):
        self.tr = Translate()

        self.delete_options = [
            ("delete word", self.delete_word),
            ("quit", Menu.CLOSE)
        ]
        self.delete_menu = Menu(
            options=self.delete_options,
            title='delete_word',
            message='',
            prompt='>',
        )
        self.main_options = [
            ("translate", self.translate),
            ("show dict", self.show_dictionary),
            ("delete word", self.delete_menu.open),
            ("quit", Menu.CLOSE)
        ]
        self.main_menu = Menu(
            options=self.main_options,
            title='main_menu',
            message='',
            prompt='> ',
            auto_clear=True
        )

    def translate(self):
        while True:
            origin_text = input("input text: ")
            if origin_text == 'quit':
                return
            try:
                translated = self.tr.translate(origin_text, True)
                print("translated: " + translated.text)
            except Exception as err:
                print("CLI Translation Error: " + str(err))

    def show_dictionary(self):
        while True:
            try:
                words = self.tr.get_full_dict()
                for word in words:
                    print(word)
                input()
                return
            except Exception as err:
                print("CLI show dictionary Error: " + str(err))

    def delete_word(self):
        while True:
            try:
                print()
                words = self.tr.get_full_dict()
                for document in words:
                    print(document)
                word_id = input("input word id: ")
                if word_id == 'quit':
                    return
                word = self.tr.get_word(word_id)
                self.tr.delete_word(word_id)
                print("word  '{}':'{}'  with  id '{}'  deleted".format(word[1], word[2], word[0]))
                input()
            except Exception as e:
                print("CLI delete word Error: " + str(e))

    def run(self):
        self.main_menu.open()
