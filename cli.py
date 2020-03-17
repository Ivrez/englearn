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
            ("show dict", self.show_dictionary),
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
            except Exception as e:
                print("Translation Error: ", e)

    def show_dictionary(self):
        while True:
            try:
                words = self.tr.show_dictionary()
                for i in words:
                    #print(i)
                    print("{} {} {} {}".format(i[0], i[1], i[2], i[3]))
                input()
                return
            except Exception as e:
                self.main_menu.set_message("Show Dictionary Error: " + str(e))

    def run(self):
        self.main_menu.open()
