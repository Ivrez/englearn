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
            ("translate", self.translate),
            ("quit", Menu.CLOSE)
        ]

        self.main_menu = Menu(
            options=self.options,
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
            except Exception:
                print("TRANSLATION ERROR")

    def run(self):
        self.main_menu.open()
