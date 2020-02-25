from __future__ import print_function

from builtins import str
from builtins import input
from builtins import object
from menu import Menu

from translate import Translate

class CLI():
    def __init__(self):
        self.tr = Translate()

        self.options = [
            ("translate_en_to_ru", self.translate_en_to_ru),
            ("translate_ru_to_en", self.translate_ru_to_en),
            ("quit", Menu.CLOSE)
        ]

        self.main_menu = Menu(
            options=self.options,
            title="main_menu",
            prompt='>',
        )

    def translate_en_to_ru(self):
        word = input("word: ")
        return self.tr.translate_en_to_ru(word)

    def translate_ru_to_en(self):
        word = input("слово: ")
        return self.tr.translate_ru_to_en(word)

    def run(self):
        self.main_menu.open()
