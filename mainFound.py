import json
import os
import bs4
import requests
import sys
from model import FondiModel
from worker import *


import time
#from control.control import Control
#from curses.ascii import controlnames
from mainWindow import Ui_MainWindow
from PyQt6 import QtCore,QtWidgets
from PyQt6.QtCore import Qt,QAbstractTableModel, QModelIndex
# from PyQt6.QtGui import QImage
# from PyQt6.QtGui import QColor,QAction,QIcon
from PyQt6.QtWidgets import QApplication, QTableView, QMainWindow, QVBoxLayout, QWidget, QAbstractItemView, QTableWidget
from PyQt6.QtCore import QRunnable,QObject, QThreadPool, QTimer, pyqtSlot,pyqtSignal

basedir = os.path.dirname(__file__)

tick = QImage(os.path.join(basedir, "tick.png"))
datafile = os.path.join(basedir,"config", "isin.json")

#riga di commando per convertire file ui in file py
#pyuic6 mainwindow.ui -o MainWindow.py








class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.setWindowTitle("Tabella Fondi")
        self.data = self.load()
        self.model = FondiModel(self.data)
        self.tableView.setModel(self.model)
        self.model.addColumn("Somma", 0.0)
        self.updateButton.clicked.connect(self.execute)
        self.threadpool = QThreadPool()
        thread_count = self.threadpool.maxThreadCount()
        print(f"Multithreading with maximum {thread_count} threads")
        # self.tableView.setEditTriggers(QAbstractItemView.doubleClicked(index.row))

        # worker.updated.connect(self.model.aggiornaRiga,)
        # worker.signals.result.connect(self.print_output)

        # worker.signals.progress.connect(self.on_progress)

        # worker.signals.progress.connect(self.progress_fn)
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
        # self.saveButton.pressed.connect(self.save)

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

        self.timer = QTimer()
        self.timer.setInterval(1000)
        #self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()


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


    def execute(self):
        worker = Worker(self.aggiornaDati,self.data)
        # worker.signals.finished.connect(self.model.aggiornaRiga)
        # worker.signals.result.connect(self.on_result)
        worker.signals.error.connect(self.on_error)
        worker.signals.finished.connect(self.on_finished)
        worker.signals.progress.connect(self.updateProgress)
        self.threadpool.start(worker)


    def updateProgress(self,progress):
        self.progressBar.setValue(progress)

    def on_error(self):
        exctype, value, tb = error_tuple
        print("Errore:", value)
        print(tb)

    def on_finished(self):
        self.lineEdit_status.setText("Completato")


    # def recurring_timer(self):
    #     self.counter += 1
    #     self.label.setText(f"Counter: {self.counter}")

    def aggiornaDati(self, data,progress_callback=None):
        for row, fondo in enumerate(data):
            self.scarica_dati(fondo["isin"])
            totale=len(data)
            if progress_callback:
                progress=int((row+1)*100/totale)
                progress_callback.emit(progress)

    def scarica_dati(self, isin):
        url = "https://www.boursorama.com/bourse/opcvm/cours/" + isin
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
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
            self.model.name_list.append(name.text.strip())
            self.model.price_list.append(''.join(price.text.split()))
            self.model.f_Price = float(price.text.replace(",", "."))
            # self.model.prezzoAttuale = (float)(data["fondi"][i]["qta"]) * f_Price
            # self.model.guadagno += prezzoAttuale - (float)(data["fondi"][i]["investment"])
            # return  self.model.prezzoAttuale
        except:
            self.model.name_list.append('NA')
            self.model.price_list.append('NA')


##############main windows#####################################################




if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()
    window.show()
    app.exec()
