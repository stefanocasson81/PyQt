from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtWidgets import QApplication, QTableView

class MyModel(QAbstractTableModel):

    def __init__(self):
        super().__init__()
        self._data = [
            ["Mario", 25],
            ["Luca", 30],
            ["Anna", 22]
        ]

    # 📦 numero righe
    def rowCount(self, parent=None):
        return len(self._data)

    # 📦 numero colonne
    def columnCount(self, parent=None):
        return len(self._data[0])

    # 📊 dati da mostrare
    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    # 🧾 intestazioni
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                headers = ["Nome", "Età"]
                return headers[section]

    # ✏️ modifica dati
    def setData(self, index, value, role):
        if role == Qt.EditRole:
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    # 🧱 abilita editing
    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable


# 🚀 Avvio app
app = QApplication([])

view = QTableView()
model = MyModel()

view.setModel(model)
view.show()

app.exec_()