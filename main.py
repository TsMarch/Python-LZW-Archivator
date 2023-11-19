from PyQt5 import QtCore, QtWidgets
import sys
import LZW_algorithm
from LZW_algorithm import Archivator


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()



    def qo_second_window(self):
        self.secondWindow.show()
        self.hide()

    def qo_main_window(self):
        self.show()
        self.secondWindow.hide()

    def the_button_was_clicked(self):
        LZW_algorithm.Archivator.start_programm()


def main_menu():
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    window.resize(500, 500)
    app.exec()

main_menu()