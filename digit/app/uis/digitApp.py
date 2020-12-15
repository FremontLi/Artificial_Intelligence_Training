from PyQt5.QtWidgets import QApplication
from app.uis.digitFrame import DigitFrame
import sys


class DigitApp(QApplication):
    def __init__(self):
        super(DigitApp, self).__init__(sys.argv)
        self.dlg = DigitFrame()
        self.dlg.show()

