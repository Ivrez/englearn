from __future__ import print_function

from builtins import str
from builtins import input
from builtins import object
from menu import Menu

from translate import Translate
from db import DefaultDB

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
        origin_text = input("input text: ")
        translated = self.tr.translate(origin_text)
        self.main_menu.set_message("translated: " + translated)

    def run(self):
        self.main_menu.open()
