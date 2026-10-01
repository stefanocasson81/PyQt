# import sys
# from PyQt6.QtWidgets import (
#     QApplication, QMainWindow, QTableView, QWidget,
#     QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox,
# )
from PyQt6.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
import os
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import QObject, pyqtSignal

class dataBaseSql(QObject):
    messaggio = pyqtSignal(str)

    def __init__(self, fileName):
        super().__init__()
        self.nome_file = str(fileName)

    def apri_database(self):
        """Crea (o apre) il file SQLite."""
        basedir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(basedir, str(self.nome_file))
        if os.path.exists(db_path):
            self.messaggio.emit("Database esistente")
            print("Database esistente")
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName(self.nome_file)
            if db.open():
                self.messaggio.emit("File Dataase Aperto correttamente")
                print("File Dataase Aperto correttamente")
        else:
            print("Database non esistente, verrà creato")
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName(self.nome_file)
            if db.open():
                ok = self.crea_tabella()
            else:
                print("Database non esistente")
                self.messaggio.emit("Database non esistente")


        # db = QSqlDatabase.addDatabase("SQLITE")
        #
        # # db.setDatabaseName(os.path.join(basedir, self.nome_file))
        # db.setDatabaseName(self.nome_file)
        # if db.open():
        #     # if not os.path.exists(os.path.join(basedir, self.nome_file)):
        #     if not os.path.exists(self.nome_file)):
        #         ok = self.crea_tabella()
        #     else:
        #         return True
        # return False



    def crea_tabella(self):
        """Definisci qui le colonne (voci) del tuo database."""
        query = QSqlQuery()
        ok = query.exec("""
            CREATE TABLE IF NOT EXISTS fondi (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                prezzo    REAL NOT NULL DEFAULT 0.0 CHECK (prezzo >= 0),
                data      TEXT NOT NULL
                )
        """)
        if not ok:
            self.messaggio.emit("Errore creazione tabella:", query.lastError().text())
            print("Errore creazione tabella:", query.lastError().text())
            return False
        else:
            return True

    def aggiornaPrezzo(self, id_fondo, prezzo, data):
        query = QSqlQuery()
        query.prepare("UPDATE fondi SET prezzo = ?,data = ?, WHERE id = ?")
        query.addBindValue(prezzo)
        query.addBindValue(data)
        query.addBindValue(id_fondo)
        if(not query.exec()):
            self.messaggio.emit("Errore aggiunta fondi:", query.lastError().text())
            print("Errore aggiunta fondi:", query.lastError().text())
            return False
        if query.numRowsAffected() == 0:
            self.messaggio.emit("Nessun fondo con id", id_fondo)
            print("Nessun fondo con id", id_fondo)
            return False
        return True


    def inserisci_prodotto(self,prezzo,data):
        query = QSqlQuery()
        query.prepare(
            "INSERT INTO fondi (prezzo, data) VALUES (?, ?) "
        )
        query.addBindValue(prezzo)
        query.addBindValue(data)
        if not query.exec():
            self.messaggio.emit("Errore inserimento:", query.lastError().text())
            print("Errore inserimento:", query.lastError().text())
            return False
        else:
            self.messaggio.emit("Table Created successfully")
            print("Table Created successfully")
        return True


    def tabella_vuota(self):
        query = QSqlQuery("SELECT COUNT(*) FROM prodotti")
        query.next()
        return query.value(0) == 0


# class Finestra(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Magazzino")
#         self.resize(650, 400)
#
#         # Modello collegato direttamente alla tabella
#         self.model = QSqlTableModel(self)
#         self.model.setTable("prodotti")
#         self.model.setEditStrategy(
#             QSqlTableModel.EditStrategy.OnFieldChange  # salva ad ogni modifica
#         )
#         self.model.select()
#         for i, titolo in enumerate(["ID", "Nome", "Categoria", "Quantità", "Prezzo"]):
#             self.model.setHeaderData(i, Qt_Horizontal, titolo)
#
#         self.vista = QTableView()
#         self.vista.setModel(self.model)
#         self.vista.setColumnHidden(0, True)  # nasconde l'ID
#         self.vista.resizeColumnsToContents()
#
#         btn_aggiungi = QPushButton("Aggiungi riga")
#         btn_aggiungi.clicked.connect(self.aggiungi_riga)
#         btn_elimina = QPushButton("Elimina riga selezionata")
#         btn_elimina.clicked.connect(self.elimina_riga)
#
#         bottoni = QHBoxLayout()
#         bottoni.addWidget(btn_aggiungi)
#         bottoni.addWidget(btn_elimina)
#
#         layout = QVBoxLayout()
#         layout.addWidget(self.vista)
#         layout.addLayout(bottoni)
#         centrale = QWidget()
#         centrale.setLayout(layout)
#         self.setCentralWidget(centrale)
#
#     def aggiungi_riga(self):
#         if inserisci_prodotto("Nuovo prodotto", "", 0, 0.0):
#             self.model.select()
#
#     def elimina_riga(self):
#         indice = self.vista.currentIndex()
#         if not indice.isValid():
#             QMessageBox.information(self, "Attenzione", "Seleziona una riga.")
#             return
#         self.model.removeRow(indice.row())
#         self.model.select()
#
#
# from PyQt6.QtCore import Qt
# Qt_Horizontal = Qt.Orientation.Horizontal


# def main():
#     app = QApplication(sys.argv)
#
#     if apri_database() is None or not crea_tabella():
#         sys.exit(1)
#
#     if tabella_vuota():  # dati di esempio al primo avvio
#         inserisci_prodotto("Vite M6", "Ferramenta", 500, 0.05)
#         inserisci_prodotto("Cacciavite", "Utensili", 40, 4.90)
#         inserisci_prodotto("Guanti da lavoro", "Sicurezza", 25, 3.50)
#
#     finestra = Finestra()
#     finestra.show()
#     sys.exit(app.exec())
#
#
# if __name__ == "__main__":
#     main()