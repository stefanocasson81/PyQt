import time
from PyQt6.QtCore import QRunnable, QThreadPool, QTimer, pyqtSlot

class Worker(QRunnable):
    @pyqtSlot()
    def run(self):
        print("Thread started")
        time.sleep(1)
        print("Thread Complete")