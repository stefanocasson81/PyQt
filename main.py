import os
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.uic.properties import QtWidgets
from mainWindow import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.show()

app = QApplication(sys.argv)
app.setStyle('Fusion')
window = MainWindow()
window.show()
app.exec()

'''        
basedir = os.path.dirname(__file__)
app = QApplication(sys.argv)
window = uic.loadUi(os.path.join(basedir, "mainWindow.ui"))
window.show()
app.exec()
'''

