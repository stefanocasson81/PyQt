import json
import os
import bs4
import requests
import sys
#from control.control import Control
#from curses.ascii import controlnames
from mainWindow import Ui_MainWindow
from PyQt6 import QtCore,QtWidgets
from PyQt6.QtCore import Qt,QAbstractTableModel, QModelIndex
from PyQt6.QtGui import QImage
from PyQt6.QtGui import QColor,QAction,QIcon
from PyQt6.QtWidgets import QApplication, QTableView, QMainWindow, QVBoxLayout, QWidget

basedir = os.path.dirname(__file__)

tick = QImage(os.path.join(basedir, "tick.png"))
datafile = os.path.join(basedir,"config", "isin.json")



class FondiModel(QAbstractTableModel):
    def __init__(self,json_data=None):
        #super(FondiModel,self).__init__()
        super().__init__()
        #self._json_data = json_data or {}
        self._json_data =  json_data["fondi"]
        self._columns = list(self._json_data[0].keys())



    # def rowCount(self, parent=QModelIndex()):
    #     return len(self._json_data)
    #
    # def columnCount(self, parent=QModelIndex()):
    #     return len(self._headers)
    def rowCount(self, parent=None):
        return len(self._json_data)

    def columnCount(self, parent=None):
        #return len(self._json_data[0])
        return len(self._columns)

    def data(self,index,role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.ItemDataRole.DisplayRole:
            row = index.row()
            #col = index.column()
            #col_name = self._columns[0]
            column_key = index.column()
            key= self._columns[column_key]
            value = self._json_data[row].get(key)


            #return str(self._json_data[row][col_name])
            # row = self._json_data[index.row()]
            # column_key = self._json_data[index.column()]
            # return self._json_data[index.row()][index.column()]
            if isinstance(value,float):
             return "%.2f" % value
            #
            if isinstance(value,str):
             return str(value)
            return None
        if (role == Qt.ItemDataRole.BackgroundRole and index.column() == 2):
            return QColor(Qt.GlobalColor.blue)


    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return str(self._columns[section]).capitalize()
        return super().headerData(section, orientation, role)

class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.setWindowTitle("Tabella Fondi")
        # self.resize(800,600)
        # self.table = QTableView()
        data = self.load()
        self.model = FondiModel(data)
        self.tableView.setModel(self.model)
        # layout = QVBoxLayout()
        # layout.addWidget(self.table)

        # 1. Creazione della Menu Bar
        # menubar = self.menuBar()

        # 2. Aggiunta dei menu (File, Modifica)
        # fileMenu = menubar.addMenu('&File')
        # editMenu = menubar.addMenu('&Modifica')

        # 3. Creazione delle azioni (Action)
        # Azione Esci
        # exitAction = QAction(QIcon('exit.png'), '&Esci', self)
        # exitAction.setShortcut('Ctrl+Q')
        # exitAction.setStatusTip('Esci dall\'applicazione')
        self.actionExit.triggered.connect(self.close) # Connessione del segnale
        self.addButton.pressed.connect(self.add)
        # Azione Nuovo
        # newAction = QAction('&Nuovo', self)
        # newAction.triggered.connect(self.nuova_azione)

        # 4. Aggiunta delle azioni ai menu
        # fileMenu.addAction(newAction)
        # fileMenu.addSeparator() # Aggiunge una linea divisoria
        # fileMenu.addAction(exitAction)

        # self.statusBar() # Abilita la barra di stato per lo statusTip

        # container=QWidget()
        # container.setLayout(layout)
        # self.setCentralWidget(container)

    def load(self):
        try:
            with open(datafile, "r", encoding="utf-8") as f:
                #self.model.json_data = json.load(f)
                #print(self.model.json_data)
                return json.load(f)
        except FileNotFoundError:
            print("Il file non esiste.")

        except json.JSONDecodeError:
            print("Il file non contiene un JSON valido.")

        except Exception as e:
            print(f"Errore imprevisto: {e}")


    def save(self):
        with open(datafile, "w") as f:
            json.dump(self.model.todos, f)

    def add(self):
        text = self.lineEdit.text()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()
    window.show()
    app.exec()
