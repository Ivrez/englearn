import sys

from cli import CLI

class Main():
    def __init__(self):
        print('Englearn CLI app')
        cl = CLI()
        cl.run()



if __name__ == "__main__":
    Main()
