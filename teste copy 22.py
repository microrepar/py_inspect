import sys                                                                  
from PySide2.QtCore import QObject, Slot, Signal, QThread

from PySide2.QtWidgets import QApplication, QWidget



# Create the Slots that will receive signals
@Slot(str)
def update_a_str_field(message):
    print(message)

@Slot(int)
def update_a_int_field(value):
    print(value)


# Signals must inherit QObject                              
class Communicate(QObject):                                                 
    signal_str = Signal(str)
    signal_int = Signal(int)


class WorkerThread(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.signals = Communicate()
        # Connect the signals to the main thread slots
        self.signals.signal_str.connect(update_a_str_field)
        self.signals.signal_int.connect(update_a_int_field)

    def run(self):
        self.signals.signal_int.emit(1)
        self.signals.signal_str.emit("Hello World.")
        


if __name__ == "__main__":
    app = QApplication(sys.argv)    
    w = WorkerThread()
    w.start()
    sys.exit(app.exec_())