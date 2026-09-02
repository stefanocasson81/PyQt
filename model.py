# from PyQt6.QtWidgets import QApplication, QTableView, QMainWindow, QVBoxLayout, QWidget, QAbstractItemView, QTableWidget
# from PyQt6.QtCore import QRunnable,QObject, QThreadPool, QTimer, pyqtSlot,pyqtSignal
# from PyQt6.QtGui import QImage
# from PyQt6.QtGui import QColor,QAction,QIcon
# from PyQt6.QtWidgets import QApplication, QTableView, QMainWindow, QVBoxLayout, QWidget, QAbstractItemView, QTableWidget
# from PyQt6.QtCore import QRunnable,QObject, QThreadPool, QTimer, pyqtSlot,pyqtSignal
from PyQt6.QtCore import Qt,QAbstractTableModel, QModelIndex

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

    def setValue(self, isn, column_name, value):
        row = 0
        for campo in self._json_data:
            if campo["isin"] in isn:
                # if not (0 <= row < self.rowCount()):
                #     return False
                if column_name not in self._columns:
                    return False
                col = self._columns.index(column_name)
                self._json_data[row][column_name] = value
                index = self.index(row, col)
                self.dataChanged.emit(index, index)
                return True
            row = row + 1


    def aggiornaRiga(self,row,dati):
        # for row in self._json_data:
        #     row[name] = default
        for campo, valore in dati.items():
            self._json_data[row][campo] = valore

        left = self.index(row, 0)
        right = self.index(row, self.columnCount() - 1)

        self.dataChanged.emit(left, right)


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