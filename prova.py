
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