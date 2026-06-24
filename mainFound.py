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
from PyQt6.QtWidgets import QApplication, QTableView, QMainWindow, QVBoxLayout, QWidget, QAbstractItemView, QTableWidget

basedir = os.path.dirname(__file__)

tick = QImage(os.path.join(basedir, "tick.png"))
datafile = os.path.join(basedir,"config", "isin.json")

#riga di commando per convertire file ui in file py
#pyuic6 mainwindow.ui -o MainWindow.py

class FondiModel(QAbstractTableModel):
    def __init__(self,json_data=None):
        #super(FondiModel,self).__init__()
        super().__init__()
        #self._json_data = json_data or {}
        self._json_data =  json_data or {}
        self._columns = list(self._json_data[0].keys())
        self.url = 'https://www.boursorama.com/bourse/opcvm/cours/'

        self.name_list = []
        self.price_list = []
        self.date_list = []
        self.guadagno = 0.0

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
            column_key = index.column()
            key = self._columns[column_key]
            value = self._json_data[row].get(key)
            if key == "isin":
                res = requests.get(self.url+ value, headers={'User-Agent': 'Mozilla/5.0'})
                # Checking for Bad download
                try:
                    res.raise_for_status()
                except Exception as exc:
                    print("There was a problem: %s" % (exc))

                    # making soup
                soup_res = bs4.BeautifulSoup(res.text, 'html.parser')
                try:
                    # if sys.argv[-2] =='-ft':
                    #     name = soup_res.find('h1', {'class':'mod-tearsheet-overview__header__name mod-tearsheet-overview__header__name--large'})
                    #     price = soup_res.find('span',{'class':'mod-ui-data-list__value'})
                    #     name_list.append(name.text)
                    #     price_list.append(price.text.replace(',', ''))
                    # else:
                    name = soup_res.find('a', {'class': 'c-faceplate__company-link'})
                    price = soup_res.find('span', {'class': 'c-instrument c-instrument--last'})
                    self.name_list.append(name.text.strip())
                    self.price_list.append(''.join(price.text.split()))
                    self.f_Price = float(price.text.replace(",", "."))
                    prezzoAttuale = (float)(data["fondi"][i]["qta"]) * self.f_Price
                    self.guadagno += prezzoAttuale - (float)(data["fondi"][i]["investment"])
                except:
                    self.name_list.append('NA')
                    self.price_list.append('NA')


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

    def add_element(self,nuovo):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._json_data.append(nuovo)
        self.endInsertRows()

    def setData(self,index,value,role):
        if role == Qt.ItemDataRole.EditRole:
            self._json_data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def flags(self, index):
        return (
                Qt.ItemFlag.ItemIsSelectable
                | Qt.ItemFlag.ItemIsEnabled
                | Qt.ItemFlag.ItemIsEditable
        )



class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.setWindowTitle("Tabella Fondi")
        data = self.load()
        self.model = FondiModel(data)
        self.tableView.setModel(self.model)
        # self.tableView.setEditTriggers(QAbstractItemView.doubleClicked(index.row))

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
        self.saveButton.pressed.connect(self.save)

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
        with open(datafile, "w",encoding="utf-8") as f:
            # Fondi= {"Fondi": self.model._json_data}
            string_data=json.dump(self.model._json_data, f,indent=4, ensure_ascii=False)
            print(string_data)

    def add(self):
        text_isin = self.lineEdit_isin.text()
        text_desc = self.lineEdit_desc.text()
        float_qta = float(self.lineEdit_qta.text())
        float_inv = float(self.lineEdit_inv.text())
        new = {"isin" :text_isin,"desc":text_desc,"qta":float_qta,"investment":float_inv}
        self.model.add_element(new)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()
    window.show()
    app.exec()
