from PyQt5.QtWidgets import QApplication
import sys
class MirrorApp(QApplication):
    def __init__(self):
        super(MirrorApp, self).__init__(sys.argv)