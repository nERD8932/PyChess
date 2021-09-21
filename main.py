import MainMenu
from multiprocessing import freeze_support

if __name__ == "__main__":
    freeze_support()
    menuexec = MainMenu.MainMenu()
    menuexec.runMenu()
