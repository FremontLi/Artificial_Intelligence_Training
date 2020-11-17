import time
import sys
from PyQt5.QtWidgets import QApplication,QWidget
app = QApplication(sys.argv)
box = QWidget()
box.resize(250,250)
box.move(300,300)
box.setWindowTitle("box")
box.show()
sys.exit(app.exec_())