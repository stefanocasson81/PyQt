import os
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow,QMessageBox
from PyQt6.uic.properties import QtWidgets
from mainWindow import Ui_MainWindow
from PyQt6.QtGui import QAction, QIcon

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.show()


class EsempioMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Esempio Menu PyQt6')
        self.setGeometry(100, 100, 400, 300)

        # 1. Creazione della Menu Bar
        menubar = self.menuBar()

        # 2. Aggiunta dei menu (File, Modifica)
        fileMenu = menubar.addMenu('&File')
        editMenu = menubar.addMenu('&Modifica')

        # 3. Creazione delle azioni (Action)
        # Azione Esci
        exitAction = QAction(QIcon('exit.png'), '&Esci', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Esci dall\'applicazione')
        exitAction.triggered.connect(self.close) # Connessione del segnale

        # Azione Nuovo
        newAction = QAction('&Nuovo', self)
        newAction.triggered.connect(self.nuova_azione)

        # 4. Aggiunta delle azioni ai menu
        fileMenu.addAction(newAction)
        fileMenu.addSeparator() # Aggiunge una linea divisoria
        fileMenu.addAction(exitAction)

        self.statusBar() # Abilita la barra di stato per lo statusTip

    def nuova_azione(self):
        QMessageBox.information(self, 'Info', 'Azione "Nuovo" cliccata!')

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    #window = MainWindow()
    window =EsempioMenu()
    window.show()
    app.exec()

if main() == '__main__':
    main()

'''        
basedir = os.path.dirname(__file__)
app = QApplication(sys.argv)
window = uic.loadUi(os.path.join(basedir, "mainWindow.ui"))
window.show()
app.exec()
'''

