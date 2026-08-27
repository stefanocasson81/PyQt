import json
import os
import bs4
import requests
import sys
import time
#from control.control import Control
#from curses.ascii import controlnames
from mainWindow import Ui_MainWindow
from PyQt6 import QtCore,QtWidgets
from PyQt6.QtCore import Qt,QAbstractTableModel, QModelIndex
from PyQt6.QtGui import QImage
from PyQt6.QtGui import QColor,QAction,QIcon
from PyQt6.QtWidgets import QApplication, QTableView, QMainWindow, QVBoxLayout, QWidget, QAbstractItemView, QTableWidget
from PyQt6.QtCore import QRunnable, QThreadPool, QTimer, pyqtSlot

basedir = os.path.dirname(__file__)

tick = QImage(os.path.join(basedir, "tick.png"))
datafile = os.path.join(basedir,"config", "isin.json")

#riga di commando per convertire file ui in file py
#pyuic6 mainwindow.ui -o MainWindow.py


########################################model##################################


class FondiModel(QAbstractTableModel):
    def __init__(self,json_data=None):
        #super(FondiModel,self).__init__()
        super().__init__()
        self._json_data =  json_data or {}
        self._columns = list(self._json_data[0].keys())
        self.url = 'https://www.boursorama.com/bourse/opcvm/cours/'

        self.name_list = []
        self.price_list = []
        self.date_list = []
        self.guadagno = 0.0
        self.somma = 0
        self.f_Price = 0

    # def rowCount(self, parent=QModelIndex()):
    #     return len(self._json_data)
    #
    # def columnCount(self, parent=QModelIndex()):
    #     return len(self._headers)
    def rowCount(self, parent=None):
        return len(self._json_data)

    def columnCount(self, parent=None):
        return len(self._columns)

    # def insertColumns(self,columns):
    #     self.beginInsertColumns(QModelIndex(), self.columnCount(), self.columnCount())
    #     self._json_data.append(f"{"Somma"}")
    #     self.endInsertColumns()

    def addColumn(self, name, default=None):
        if name in self._columns:
            return
        pos = self.columnCount()
        self.beginInsertColumns(QModelIndex(), pos, pos)
        self._columns.append(name)
        for row in self._json_data:
            row[name] = default
        self.endInsertColumns()

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            key = self._columns[index.column()]
            value = self._json_data[index.row()].get(key)

            if isinstance(value, float):
                return f"{value:.2f}"

            if isinstance(value, str):
                return str(value)

            return value

        return None



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
            key = self._columns[index.column()]
            self._json_data[index.row()][key] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    # def setData(self, row, column_name, value):
    #     self._json_data[row][column_name] = value
    #     column = self._columns.index(column_name)
    #     index = self.index(row, column)
    #     self.dataChanged.emit(index, index)

    def setColumn(self, name, values):
        if len(values) != self.rowCount():
            return
        column = self._columns.index(name)
        for row, value in enumerate(values):
            self._json_data[row][name] = value
        top = self.index(0, column)
        bottom = self.index(self.rowCount() - 1, column)
        self.dataChanged.emit(top, bottom)

    def flags(self, index):
        return (
                Qt.ItemFlag.ItemIsSelectable
                | Qt.ItemFlag.ItemIsEnabled
                | Qt.ItemFlag.ItemIsEditable
        )


###################worker######################

# class WorkerSignals(QObject):
    """Signals from a running worker thread.

    finished
        int thread_id

    error
        tuple (exctype, value, traceback.format_exc())

    result
        object data returned from processing, anything

    progress
        tuple (thread_id, progress_value)
    """

    # finished = pyqtSignal(int)  # thread_id
    # error = pyqtSignal(tuple)
    # result = pyqtSignal(object)
    # progress = pyqtSignal(tuple)  # (thread_id, progress_value)

class Worker(QRunnable):
    """Worker thread.

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread.
                     Supplied args and kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function
    """
    # def __init__(self, fn, *args, **kwargs):
    def init(self):
        super().__init__()
        # self.fn = fn
        # self.args = args
        # self.kwargs = kwargs
        # # self.signals = WorkerSignals()
        # self.thread_id = kwargs.get("thread_id", 0)
        # # Add the callback to our kwargs
        # self.kwargs["progress_callback"] = self.signals.progress

    @pyqtSlot()
    def run(self):
        # try:
        #     result = self.fn(*self.args, **self.kwargs)
        # except Exception:
        #     traceback.print_exc()
        #     exctype, value = sys.exc_info()[:2]
        #     self.signals.error.emit((exctype, value, traceback.format_exc()))
        # else:
        #     self.signals.result.emit(result)
        # finally:
        #     self.signals.finished.emit(self.thread_id)
        print("Thread start")
        # time.sleep(0.5)
        print("Thread complete")
###############main windows#####################################################


class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.setWindowTitle("Tabella Fondi")
        data = self.load()
        self.model = FondiModel(data)
        self.tableView.setModel(self.model)
        self.model.addColumn("Somma", 0.0)
        self.threadpool = QThreadPool()
        # self.tableView.setEditTriggers(QAbstractItemView.doubleClicked(index.row))
        worker = Worker()
        self.threadpool.start(worker.run)


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

        self.timer = QTimer()
        self.timer.setInterval(1000)
        #self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()
        self.threadpool = QThreadPool()
        thread_count = self.threadpool.maxThreadCount()
        print(f"Multithreading with maximum {thread_count} threads")

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


    def start_worker(self):
        worker = Worker()
        self.threadpool.start(worker)


    def progress_fn(self, data):
        thread_id, n = data
        print(f"THREAD #{thread_id}: {n:.1f}% done")


    def print_output(self, s):
        print(s)

    def thread_complete(self, thread_id):
        print(f"THREAD #{thread_id} COMPLETE!")

    def oh_no(self):
        # Pass the function to execute
        self.thread_id += 1
        worker = Worker(
            self.execute_this_fn, thread_id=self.thread_id
        )  # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)
        # Execute
        self.threadpool.start(worker)

    def recurring_timer(self):
        self.counter += 1
        self.label.setText(f"Counter: {self.counter}")

    def execute_this_fn(self, progress_callback, thread_id):
        for n in range(0, 5):
            time.sleep(1)
            progress = n * 100 / 4
            progress_callback.emit((thread_id, progress))
        return "Done."

    def recurring_timer(self):
        self.counter += 1
        self.label.setText(f"Counter: {self.counter}")

    def aggiornaDati(self,fondi):
        for row, fondo in enumerate(fondi):
            dati = scarica_dati(fondo["isin"])

            self.updated.emit(row, dati)

        self.finished.emit()

    def scarica_dati(self,isin):

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
            self.model.prezzoAttuale = (float)(data["fondi"][i]["qta"]) * f_Price
            self.model.guadagno += prezzoAttuale - (float)(data["fondi"][i]["investment"])
        except:
            self.model.name_list.append('NA')
            self.model.price_list.append('NA')



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()
    window.show()
    app.exec()
