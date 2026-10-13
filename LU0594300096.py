import sys
import os
import datetime as dt
import time
import os
os.environ["SELENIUM_DRIVER_WAIT_TIME"] = "15"   # prima dell'import di mstarpy
import mstarpy as ms        # resta prima di PyQt6
from mstarpy import Funds                      # importato prima di PyQt6
from PyQt6.QtCore import QCoreApplication
from PyQt6.QtSql import QSqlDatabase, QSqlQuery

DB = "fondi.db"
ISINS = ["LU0594300096"]
DATA_INIZIO = dt.date(2011, 1, 1)

def scarica_nav(fondo, inizio, tentativi=3, attesa=10):
    for n in range(1, tentativi + 1):
        try:
            return fondo.nav(
                start_date=dt.datetime.combine(inizio, dt.time.min),
                end_date=dt.datetime.today(),
                frequency="daily",
            )
        except ConnectionError as e:
            print(f"  tentativo {n}/{tentativi} fallito: {str(e)[:60]}", flush=True)
            if n == tentativi:
                raise
            time.sleep(attesa)


def esegui(db, sql, params=()):
    q = QSqlQuery(db)
    q.prepare(sql)
    for p in params:
        q.addBindValue(p)
    if not q.exec():
        raise RuntimeError(f"{q.lastError().text()} | SQL: {sql[:60]}")
    return q


def main():
    basedir = os.path.dirname(os.path.abspath(__file__))
    db = QSqlDatabase.addDatabase("QSQLITE", "conn_fondi")
    db.setDatabaseName(os.path.join(basedir, DB))
    if not db.open():
        raise RuntimeError(db.lastError().text())

    esegui(db, "CREATE TABLE IF NOT EXISTS fondi (isin TEXT PRIMARY KEY, nome TEXT)")
    esegui(db, """CREATE TABLE IF NOT EXISTS nav (
        isin TEXT NOT NULL, data TEXT NOT NULL, valore REAL NOT NULL,
        PRIMARY KEY (isin, data))""")
    session = ms.MorningstarSession()
    for isin in ISINS:
        fondo = ms.Funds(isin, session=session)
        nome = getattr(fondo, "name", None)
        print(f"{isin}: {nome}", flush=True)

        esegui(db,
               "INSERT INTO fondi (isin, nome) VALUES (?, ?) "
               "ON CONFLICT(isin) DO UPDATE SET nome = excluded.nome",
               (isin, nome))

        q = esegui(db, "SELECT MAX(data) FROM nav WHERE isin = ?", (isin,))
        ultimo = q.value(0) if q.next() else None
        q.finish()
        del q

        inizio = (dt.date.fromisoformat(ultimo) + dt.timedelta(days=1)
                  if ultimo else DATA_INIZIO)
        if inizio > dt.date.today():
            print("  già aggiornato", flush=True)
            continue

        # storico = fondo.nav(
        #     start_date=dt.datetime.combine(inizio, dt.time.min),
        #     end_date=dt.datetime.today(),
        #     frequency="daily",
        # )
        scarica_nav(fondo, inizio)
        print("  valori scaricati:", len(storico), flush=True)
        if storico:
            print("  primo elemento:", storico[0], flush=True)

        db.transaction()
        for r in storico:
            esegui(db,
                   "INSERT OR REPLACE INTO nav (isin, data, valore) VALUES (?, ?, ?)",
                   (isin, str(r["date"])[:10], float(r["nav"])))
        db.commit()
        print(f"  aggiunti {len(storico)} valori", flush=True)

    db.close()


app = QCoreApplication(sys.argv)
main()                                   # db e query sono locali: spariscono qui
QSqlDatabase.removeDatabase("conn_fondi")  # ora è sicuro rimuovere la connessione