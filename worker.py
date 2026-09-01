from PyQt6.QtCore import QRunnable,QObject,pyqtSlot,pyqtSignal
import sys

class WorkerSignals(QObject):
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

    finished = pyqtSignal()  # thread_id
    error = pyqtSignal(tuple)
    progress = pyqtSignal(int)
    # result = pyqtSignal()
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
    def __init__(self,fn, *args, **kwargs):
    # def init(self):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # self.thread_id = kwargs.get("thread_id", 0)
        # # Add the callback to our kwargs
        self.kwargs["progress_callback"] = self.signals.progress

    @pyqtSlot()
    def run(self):

        try:
            self.fn(*self.args,**self.kwargs)
        except Exception:
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.finished.emit()
