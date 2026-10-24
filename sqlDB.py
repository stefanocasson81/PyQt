# import sys
# from PyQt6.QtWidgets import (
#     QApplication, QMainWindow, QTableView, QWidget,
#     QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox,
# )
from PyQt6.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
import os
# from datetime import date
from datetime import datetime
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import QObject, pyqtSignal

class dataBaseSql(QObject):
    messaggio = pyqtSignal(str)

    def __init__(self, fileName):
        super().__init__()
        self.nome_file = str(fileName)
        # self.apri_database()

    def apri_database(self):
        """Crea (o apre) il file SQLite."""
        basedir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(basedir, str(self.nome_file))
        if os.path.exists(db_path):
            self.messaggio.emit("Database esistente")
            print("Database esistente")
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName(db_path)
            if db.open():
                self.messaggio.emit("File Database Aperto correttamente")
                print("File Dataase Aperto correttamente")
                return db
            else:
                print("Database non aperto correttamente")
                self.messaggio.emit("Database non aperto correttamente")
                return None
        else:
            print("Database non esistente, verrà creato")
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName(db_path)
            if db.open():
                ok = self.crea_tabella()
                if ok:
                    return db
                else:
                    print("Tabella non creata")
                    return None
            else:
                print("Database non esistente")
                self.messaggio.emit("Database non esistente")
                return None

    def crea_tabella(self):
        query = QSqlQuery()
        istruzioni = [
            """CREATE TABLE IF NOT EXISTS fondi (
                   id     INTEGER PRIMARY KEY,
                   isin   TEXT NOT NULL UNIQUE,
                   nome   TEXT NOT NULL,
                   valuta TEXT DEFAULT 'EUR')""",
            """CREATE TABLE IF NOT EXISTS prezzi (
                   fondo_id INTEGER NOT NULL REFERENCES fondi(id),
                   data     TEXT NOT NULL,
                   ora      TEXT,          
                   valore   REAL NOT NULL,
                   PRIMARY KEY (fondo_id, data))""",
            "CREATE INDEX IF NOT EXISTS idx_prezzi_data ON prezzi(data)",
        ]
        for sql in istruzioni:
            if not query.exec(sql):
                self.messaggio.emit(f"Errore creazione tabella: {query.lastError().text()}")
                print(f"Errore creazione tabella: {query.lastError().text()}")
                return False
        return True


    def inserisci_prodotto(self,isin, nome,valuta = "EUR"):
        query = QSqlQuery()
        query.prepare(
            "INSERT OR IGNORE INTO fondi (isin,nome,valuta) VALUES (?, ?, ?)"
        )
        query.addBindValue(isin)
        query.addBindValue(nome)
        query.addBindValue(valuta)

        ok = query.exec()
        if not ok:
            self.messaggio.emit(f"Errore inserimento: {query.lastError().text()}")
            print("Errore inserimento:", query.lastError().text())
            return None
        else:
            self.messaggio.emit("Table Created successfully")
            print("Table Created successfully")
            q = QSqlQuery()
            q.prepare("SELECT id FROM fondi WHERE isin = ?")
            q.addBindValue(isin)
            q.exec()
            if q.next():
                return q.value(0)#restituisce isin
            return None

    def trovaFondo(self,i):
        q = QSqlQuery()
        q.prepare("SELECT id FROM fondi WHERE isin = ?")
        q.addBindValue(i)
        if q.exec() and q.next():
            return q.value(0)
        return None


    def aggiornaPrezzo(self,isin, nome,valore, data=None):
        fid = self.trovaFondo(isin)
        if fid is None:
            fid = self.inserisci_prodotto(isin,nome)
            if fid is not None:
                self.messaggio.emit(f"Inserito Nuovo fondo:{isin}")
                print(f"Inserito Nuovo fondo:{isin}")
            else:
                return False

        # print("Errore aggiorna fondi:", q.lastError().text())
        # nuovoIsin = isin
        adesso = datetime.now()
        data = adesso.date().isoformat()
        ora = adesso.time().isoformat(timespec="seconds")
        # datetime.time().isoformat()
        q = QSqlQuery()
        q.prepare("INSERT INTO prezzi (fondo_id, data, ora, valore) VALUES (?, ?, ?, ?) "
                    "ON CONFLICT (fondo_id, data) DO UPDATE SET valore = excluded.valore, ora = excluded.ora"
                  )
        # q.prepare("UPDATE prezzi SET valore =? WHERE fondo_id =? AND data =?")

        # q.addBindValue(nuovoIsin)
        q.addBindValue(fid)
        q.addBindValue(data)
        q.addBindValue(ora)
        q.addBindValue(valore)

        if not q.exec():
            self.messaggio.emit(f"Errore aggiorna prezzo:{q.lastError().text()}")
            print("Errore aggiorna prezzo:", q.lastError().text())
            return False
        print(q.numRowsAffected())
        self.messaggio.emit(f"Aggiornate:{q.numRowsAffected()} righe")
        return True



    # def aggiornaPrezzo(self, id_fondo, prezzo, data=None):
    #     query = CREATE INDEX IF NOT EXISTS idx_prezzi_data ON prezzi(data);()
    #     query.prepare("UPDATE fondi SET prezzo = ?,data = ? WHERE id = ?")
    #     query.addBindValue(prezzo)
    #     query.addBindValue(data)
    #     query.addBindValue(id_fondo)
    #     if not query.exec():
    #         self.messaggio.emit(f"Errore aggiunta fondi:{query.lastError().text()}")
    #         print("Errore aggiunta fondi:", query.lastError().text())
    #         return False
    #     if query.numRowsAffected() == 0:
    #         self.messaggio.emit(f"Nessun fondo con id : {id_fondo}")
    #         print("Nessun fondo con id", id_fondo)
    #         return False
    #     return True


    def tabella_vuota(self):
        query = QSqlQuery("SELECT COUNT(*) FROM prodotti")
        query.next()
        return query.value(0) == 0

    # def salva_prezzo(fondo_id, valore, data=None):
    #     data = data or date.today().isoformat()
    #     q = QSqlQuery()
    #     q.prepare("INSERT OR IGNORE INTO prezzi (fondo_id, data, valore) "
    #               "VALUES (?, ?, ?)")
    #     q.addBindValue(fondo_id)
    #     q.addBindValue(data)
    #     q.addBindValue(valore)
    #     if not q.exec():
    #         raise RuntimeError(q.lastError().text())


    # def ultimi_valori():
    #     q = QSqlQuery("""
    #         SELECT f.nome, p.data, p.valore
    #         FROM fondi f
    #         JOIN prezzi p ON p.fondo_id = f.id
    #         WHERE p.data = (SELECT MAX(data) FROM prezzi WHERE fondo_id = f.id)
    #         ORDER BY f.nome
    #     """)
    #     righe = []
    #     while q.next():
    #         righe.append((q.value(0), q.value(1), q.value(2)))
    #     return righe


    def andamento(fondo_id):
        q = QSqlQuery()
        q.prepare("SELECT data, valore FROM prezzi WHERE fondo_id = ? ORDER BY data")
        q.addBindValue(fondo_id)
        q.exec()
        righe = []
        while q.next():
            righe.append((q.value(0), q.value(1)))
        return righe
