import sys
import time
from PySide2.QtCore import QThread
from PySide2.QtWidgets import QApplication, QPushButton, QWidget


class Loop(QThread):
    def run(self):
        while True:
            print('Estamos no loop')
            time.sleep(1)


class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__()
        self.resize(200, 200)
        self.button = QPushButton('Iniciar loop', self)
        self.button.clicked.connect(self.start_loop)
        
        self.button_ok = QPushButton('Ok', self)
        self.button_ok.move(100,0)
        self.button_ok.clicked.connect(self.ok)

    def ok(self):
        print('Olá Mundo!')

    def start_loop(self):
        self.thread_loop = Loop()
        self.thread_loop.start()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()
    sys.exit(0)
