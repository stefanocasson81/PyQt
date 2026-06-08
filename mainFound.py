import json
import os
import bs4
import requests
import sys
#from control.control import Control
#from curses.ascii import controlnames
# from mainWindow_ui import Ui_MainWindow
from PyQt6 import QtCore,QtWidgets
from PyQt6.QtCore import Qt,QAbstractTableModel, QModelIndex
from PyQt6.QtGui import QImage
from PyQt6.QtWidgets import QApplication, QTableView, QMainWindow, QVBoxLayout, QWidget

basedir = os.path.dirname(__file__)

tick = QImage(os.path.join(basedir, "tick.png"))
datafile = os.path.join(basedir,"config", "isin.json")



class FondiModel(QAbstractTableModel):
    def __init__(self,json_data=None):
        #super(FondiModel,self).__init__()
        super().__init__()
        self._json_data = json_data or {}

    # def rowCount(self, parent=QModelIndex()):
    #     return len(self._json_data)
    #
    # def columnCount(self, parent=QModelIndex()):
    #     return len(self._headers)
    def rowCount(self, parent=None):
        return len(self._json_data)

    def columnCount(self, parent=None):
        return len(self._json_data[0])

    def data(self,index,role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            row = index.row()
            #col = index.column()
            #col_name = self._columns[0]
            column_key = index.column()
            #return str(self._json_data[row][col_name])
            # row = self._json_data[index.row()]
            # column_key = self._json_data[index.column()]
            # return self._json_data[index.row()][index.column()]
            if isinstance(self._json_data[row][column_key],float):
             return "%.2f" % (row.get(column_key))
            #
            if isinstance(self._json_data[row][column_key],str):
             return str(row.get(column_key, ""))

        return None

    # def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
    #     if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
    #         return str(self._headers[section]).capitalize()
    #     return super().headerData(section, orientation, role)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.setupUi(self)
        headers=["isin","desc","qta","investment"]
        self.setWindowTitle("Tabella Fondi")
        self.resize(800,600)
        self.table = QTableView()
        data = self.load()
        self.model = FondiModel(data)
        self.table.setModel(self.model)
        layout = QVBoxLayout()
        layout.addWidget(self.table)

        container=QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
