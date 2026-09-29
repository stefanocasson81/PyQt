# import sys
# from PyQt6.QtWidgets import (
#     QApplication, QMainWindow, QTableView, QWidget,
#     QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox,
# )
from PyQt6.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from pathlib import Path
import os

class dataBaseSql():
    def __init__(self, fileName="dbValori.db"):
        self.nome_file = fileName

    def apri_database(self):
        """Crea (o apre) il file SQLite."""
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(self.nome_file)
        if not db.open():
            print("Errore apertura database:", db.lastError().text())
            return None
        return db

    def crea_database(self):
        basedir = os.path.dirname(__file__)
        if Path (self.nome_file).exists():
            return True
        db=QSqlDatabase.addDatabase("SQLITE")
        db.setDatabaseName(os.path.join(basedir, str(self.nome_file)))
        if not db.open():
            self.crea_tabella()
            return db

    def crea_tabella(self):
        """Definisci qui le colonne (voci) del tuo database."""
        query = QSqlQuery()
        ok = query.exec("""
            CREATE TABLE IF NOT EXISTS prodotti (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                prezzo      REAL    NOT NULL CHECK (prezzo >= 0),
                prezzo    REAL DEFAULT 0.0
            )
        """)
        if not ok:
            print("Errore creazione tabella:", query.lastError().text())
        return ok


    def inserisci_prodotto(nome, categoria, quantita, prezzo):
        query = QSqlQuery()
        query.prepare(
            "INSERT INTO prodotti (nome, categoria, quantita, prezzo) "
            "VALUES (?, ?, ?, ?)"
        )
        query.addBindValue(nome)
        query.addBindValue(categoria)
        query.addBindValue(quantita)
        query.addBindValue(prezzo)
        if not query.exec():
            print("Errore inserimento:", query.lastError().text())
            return False
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