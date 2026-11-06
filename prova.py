
import os
os.environ["SELENIUM_DRIVER_WAIT_TIME"] = "60"
import datetime as dt
import mstarpy as ms

session = ms.MorningstarSession()
fondo = ms.Funds("LU0594300096", session=session)
print(fondo.name)

fine = dt.datetime.today()
inizio = fine - dt.timedelta(days=10)
print(fondo.nav(inizio, fine, frequency="daily"))


from mstarpy import Funds, MorningstarSession

# Inizializza la sessione
session = MorningstarSession()

# Esempio: cerca un fondo tramite ISIN o ID Morningstar (es. fondo comune o ETF)
# Sostituisci "F000000000" con il codice Morningstar o ISIN effettivo del fondo
fondo = Funds(term="LU0011815304", country="it")

# Ottieni lo storico dei valori / NAV
df_storico = fondo.historical()
print(df_storico)

# Esporta in CSV se necessario
df_storico.to_csv("storico_morningstar.csv", index=False)