from __future__ import print_function

from builtins import str
from builtins import input
from builtins import object
from menu import Menu

from translate import Translate

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
                translated = self.tr.translate(origin_text)
                print("translated: " + translated)
                #self.main_menu.set_message("translated: " + translated)
            except Exception as e:
                print("CLI Translation Error: ", e)

    def show_dictionary(self):
        while True:
            try:
                words = self.tr.get_full_dict()
                for i in words:
                    print("{} {} {} {}".format(i[0], i[1], i[2], i[3]))
                input()
                return
            except Exception as e:
                print("CLI show dictionary Error: " + str(e))

    def delete_word(self):
        while True:
            try:
                print()
                words = self.tr.get_full_dict()
                for i in words:
                    print("{} {} {} {}".format(i[0], i[1], i[2], i[3]))
                word_id = input("input word id: ")
                if word_id == 'q':
                    return
                int(word_id)
                word = self.tr.get_word(word_id)
                self.tr.delete_word(word_id)
                print("word  '{}':'{}'  with  id '{}'  deleted".format(word[1], word[2], word[0]))
                input()
            except Exception as e:
                print("CLI delete word Error: " + str(e))

    def run(self):
        self.main_menu.open()
